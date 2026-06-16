import os
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def MCPS_List_Tools(server_url: str):
    async with AsyncExitStack() as stack:
        r, w, _ = await stack.enter_async_context(streamablehttp_client(server_url))
        session = await stack.enter_async_context(ClientSession(r, w))
        
        await session.initialize()
        resp = await session.list_tools()
        tools = resp.tools
        
        print("Tool Descriptions\n")
        for i, t in enumerate(tools, 1):
            print(f"{i}. {t.name}")
            print(f"{t.description or '(no description)'}\n")

async def main():
    MCP_SERVER_URL = "http://127.0.0.1:3333/mcp"
    await MCPS_List_Tools(MCP_SERVER_URL)

if __name__ == "__main__":
    asyncio.run(main())