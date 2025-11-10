#安装依赖
1. uv sync
2. source .venv/bin/activate

#启动mcp server
1. python mcp_server.py 

#启动agent server
1.  fastapi run main_async_api.py --port 9090

#API 说明
1. session ID申请，http:vpc_ip:9090/session/new  
客户端在向agent server发送指令前，需要先申请session_id，此id在服务端做了历史记忆能力，在调用task/run api时需传入session_id,即可在相关上下文中执行任务


2. 任务执行，http:vpc_ip:9090/task/run
入参：
    name: 任务名称
    instruct: 任务指令（如，帮我做一个补货计划）
    session_id: /session/new API返回的ID