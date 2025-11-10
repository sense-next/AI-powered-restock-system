
import uuid
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from restock_agent import RestockAgent

app = FastAPI()
agent = RestockAgent()

class TaskMeta(BaseModel):
    name: str | None = None # 任务名称
    instruct: str # 任务指令
    session_id:str 


@app.post("/task/run")
async def task_run(task: TaskMeta):
    print(f"收到“{task.name}”任务的指令[{task.instruct}]:")
    response = await agent.chat(task.instruct, session_id=task.session_id)
    return {"content":response}

@app.get("/session/new")
async def session_new():
    id = uuid.uuid4()
    print(f"创建新session id ={id}")
    return {"session_id":id}


