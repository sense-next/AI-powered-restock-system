import os
from typing import List, Dict, Any, Literal, Annotated
from typing_extensions import TypedDict
from dataclasses import dataclass
import json
from datetime import datetime
import pprint
import uuid
import asyncio


# LangGraph相关导入
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

# LangChain相关导入
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph.message import add_messages  # 导入缩减器
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


# 工具导入
from mcp_tools import get_tools_mcp


# 环境配置导入
from dotenv import load_dotenv
load_dotenv()


@dataclass
class CommonContext:
    model_url: str   
    model_name: str   
    model_key: str   

# ========== 状态定义，agent workflow共享状态==========
class AgentState(TypedDict):
    """智能体状态定义"""
    messages: Annotated[List, add_messages] 
    current_task: str# 当前任务
    task_type: str# 任务类型：chat, restock
  


# ========== 工具定义 ==========

# 工具列表
tools = get_tools_mcp()

class RecommandOut(BaseModel):
    '''应该如何补货的建议'''

    classid: str = Field(description="需补货的商品类别")
    quntity: str = Field(description="需补货的数量")
    barcode: str = Field(description="需补货的商品编码")
    
class ReasoningResponse(BaseModel):
    final_answer: str
    reasoning: str  # 这个字段将用来存放推理过程

# ========== 核心Agent类 ==========
class RestockAgent:
        """补货智能助手"""
        def __init__(self,model_name:str = "",model_url:str ="",model_key:str =""):
                """
                初始化智能助手

                Args:
               
                """

                self.model_key = model_key or os.getenv('MODEL_KEY')
                self.model_url = model_url or os.getenv('MODEL_URL')
                self.session_id = 0
                if os.getenv('REASONING') == 'true':
                        self.model_name = model_name or os.getenv('MODEL_REASONING_NAME')
                        reasoning = {
    "effort": "medium",  # 'low', 'medium', or 'high'
     # 'detailed', 'auto', or None
}
                        self.llm  = ChatOpenAI(
                        model=self.model_name,
                        temperature=0,
                        api_key=self.model_key,
                        base_url=self.model_url,
                        reasoning_effort='medium',
                        extra_body={"return_reasoning":True}
                        #response_format={type:"json_object"}
                        )
                        #elf.llm = self.llm.bind_tools(tools).with_structured_output(ReasoningResponse)

                else:
                        self.model_name = model_name or os.getenv('MODEL_NAME')
                        self.llm  = ChatOpenAI(
                        model=self.model_name,
                        temperature=0,
                        api_key=self.model_key,
                        base_url=self.model_url,
                        #response_format={type:"json_object"}
                        )
                self.llm = self.llm.bind_tools(tools)

              
                self.memory = MemorySaver()

# 创建工具节点
                self.tool_node = ToolNode(tools)

# 构建图
                self.app = self._build_graph()

                print(f"✅补货智能agent初始化完毕，使用模型: {model_name}")

        def _build_graph(self) -> StateGraph:
                """构建工作流图"""

# 创建状态图
                workflow = StateGraph(state_schema=AgentState, context_schema=CommonContext)

# 添加节点
                workflow.add_node("classifier", self._classify_task)          # 任务分类
                workflow.add_node("only_chat", self._only_chat) 
                workflow.add_node("restock", self._restock) 

                workflow.add_node("tools", self.tool_node)            
              
# 添加边和条件路由
                workflow.add_edge(START, "classifier")

# 从分类器到不同处理路径
                workflow.add_conditional_edges(
                        "classifier",
                        self._route_after_classification,
                        {
                        "only_chat": "only_chat",
                        "restock": "restock",
                        }
                )

               

# 工具调用后回到简单对话
                workflow.add_conditional_edges(
                       "restock",
                      tools_condition,
                      {
        "tools": "tools",  # 如果有，则路由到"tools"节点
        "__end__": END     # 如果没有，则结束
    }
                      )
                workflow.add_edge("tools", "restock")
                

          

                return workflow.compile(checkpointer=self.memory)

        async def _classify_task(self, state: AgentState) -> Dict[str, Any]:
                """任务分类节点"""
                messages = state.get("messages", [])
                if not messages:
                        return {"task_type": "restock"}

                last_message = messages[-1].content if messages else ""

# 使用LLM进行任务分类
                classification_prompt = f"""
                        分析用户的请求，将其分类为以下类型之一：
                        1. only_chat - 聊天
                        2. restock - 需要认真分析的SKU补货需求
                        
                        用户请求: {last_message}

                        只返回类型名称，不要其他多余文字。
        """

                response = await self.llm.ainvoke([HumanMessage(content=classification_prompt)])
             
                task_type = response.content.strip().lower()
                
                

# 验证返回值
                valid_types = ["restock"]
                if task_type not in valid_types:
                        task_type = "restock"
                print("当前任务类型:    "+ task_type)
                return {
                        "task_type": task_type,
                        "current_task": last_message,
                        "reasoning_steps": [f"任务分类: {task_type}"]
                        }

        def _only_chat(self, state: AgentState) -> Dict[str, Any]:
                """简单对话处理节点"""
                messages = state.get("messages", [])

# 构建对话提示
                system_prompt = """
                        你是一个活泼可爱的聊天助手
                        """
                system_msg = SystemMessage(content=system_prompt)
                full_messages = [system_msg] + messages
              
                response = self.llm.ainvoke(full_messages)
              
                # Response text
              

                
# Reasoning summaries
             
                return {"messages": [response] }

        async def _restock(self, state: AgentState) -> Dict[str, Any]:
                """简单对话处理节点"""
                messages = state.get("messages", [])

# 构建对话提示
                system_prompt = """
                        你是一个运营供应链的行业专家，特别擅长根据商品SKU在库存，销售，补货等环节的数据分析，最终给出一个极具专业价值的补货建议；
                        你特别善于利用工具来查询需要补货的门店的当前SKU情况，结合最近一个月内门店的销售情况，总部补货系统的最畅销商品，总部商品库存，以及单门店
                        最小的库存要求情况，来分析并合理制定补货计划，输出准确的补货建议；
                        # 任务描述与要求
                        1. 首先详细了解门店当前的商品库存情况，明确哪些商品库存较低需要补货。
                        2. 分析门店历史卖得好的商品数据，找出持续畅销或近期销量增长明显的商品。
                        3. 关注总部的新品信息，了解新品的特点、市场定位等。
                        4. 掌握总部采购量较多的商品情况，判断这些商品的市场潜力。
                        5. 综合以上多维度信息，按照重要程度进行排序，为门店推荐最合适的商品，推荐数量控制在5-10种。
                       
                        """
                system_msg = SystemMessage(content=system_prompt)
                full_messages = [system_msg] + messages
              
                response = await self.llm.ainvoke(full_messages)
              
                # Response text
              

                
# Reasoning summaries
             
                return {"messages": [response] }

               
        def _route_after_classification(self, state: AgentState) -> str:
                """分类后的路由决策"""
                task_type = state.get("task_type", "only_chat")
                return task_type

        async def chat(self, message: str, session_id: str = "default") -> str:
                """
                与智能助手对话

                Args:
                message: 用户消息
                session_id: 会话ID，用于维护对话历史

                Returns:
                str: 助手回复
                """
                try:
# 准备初始状态
                        self.initial_state = {
                        "messages": [],
                        "current_task": "",
                        "task_type": "",
                        }
                        #config = {"configurable": {"thread_id": session_id}}
                        #state = self.app.get_state(config)
                        #if state.values != {}:
                         #       for item in state.values['messages']:
                         #               if (item,HumanMessage):
                         ##                       self.initial_state['messages'] += [HumanMessage(content=item.content)]
                         #              if isinstance(item,AIMessage):
                          #                      self.initial_state['messages'] += [AIMessage(content=item.content)]
                        #else:
                        if self.session_id != session_id:
                                  self.initial_state = {
                        "messages": [HumanMessage(content=message)],
                        "current_task": "",
                        "task_type": "",
                        }
                        else:
                                pass#self.initial_state['messages'] += [HumanMessage(content=message)]

# 执行图处理
                        config = {"configurable": {"thread_id": session_id}}
                        final_state = await self.app.ainvoke(self.initial_state, config=config,
                                                      context=CommonContext(
                                                                model_key=os.getenv('MODEL_KEY'),
                                                                model_name=os.getenv('MODEL_NAME'),
                                                                model_url=os.getenv('MODEL_URL')))
    
                       
                    
# 提取回复
                       
                        messages = final_state.get("messages", [])
                      
                        if messages and isinstance(messages[-1], AIMessage):
                                return messages[-1].content
                        else:
                                return"抱歉，处理过程中出现了问题。"

                except Exception as e:
                        return f"对话处理失败: {str(e)}"

        def get_reasoning_steps(self, session_id: str = "default") -> List[str]:
                """获取推理步骤"""
                try:
                        config = {"configurable": {"thread_id": session_id}}
                        state = self.app.get_state(config)
                        return state.values.get("reasoning_steps", [])
                except:
                        return []

