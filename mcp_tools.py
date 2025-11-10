from langchain_mcp_adapters.client import MultiServerMCPClient  
from typing import List
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools


client = MultiServerMCPClient(  
    {
        # "math": {
        #     "transport": "stdio",  # Local subprocess communication
        #     "command": "python",
        #     # Absolute path to your math_server.py file
        #     "args": ["/path/to/math_server.py"],
        # },
        "weather": {
            "transport": "streamable_http",  # HTTP-based remote server
            # Ensure you start your weather server on port 8000
            "url": "http://127.0.0.1:8000/mcp",
        }
    }
)
# await with client.session("math") as session:
#     tools = await load_mcp_tools(session)

def get_tools_mcp() -> List:
    return asyncio.run(client.get_tools())
    


 