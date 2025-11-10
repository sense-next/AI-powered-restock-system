
import uuid
import asyncio

# ========== 使用示例 ==========
from restock_agent import RestockAgent
def demo_agent():
        """补货Agent 演示"""
        print("\n" + "="*60)
        print("🚀 补货智能助手演示")
        print("="*60)

# 创建智能助手
        agent = RestockAgent()
        sessionid = uuid.uuid4()
        while True:
                user_input = input("请输入内容（输入 'exit' 退出,输入'new'开启新会话）: ")
    
        # 检查退出条件
                if user_input.lower() == 'exit':
                        print("退出程序。")
                        break  # 跳出循环
                if user_input.lower() == 'new':
                        sessionid = uuid.uuid4()
                        user_input = input("已开启新会话，输入: ")
                
                print(f"\n😈 sessionid = {sessionid} 的会话处理中...")
                response = asyncio.run(agent.chat(user_input, session_id=sessionid))
                print(f"\n🤖 agent回答：")
                print(response)



        print("\n✅ 补货Agent演示完成！")


if __name__ == "__main__":
        demo_agent()
