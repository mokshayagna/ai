import os
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def Create_issue(server_url: str):
    async with AsyncExitStack() as stack:
        r, w, _ = await stack.enter_async_context(streamablehttp_client(server_url))
        session = await stack.enter_async_context(ClientSession(r, w))
        
        await session.initialize()
        resp = await session.call_tool(
            "CREATE_ISSUE", {
                "project_key": "PROM",
                "summary": "Test issue from MCP",
                "description": "This issue was created using the Jira MCP server.",
                "issue_type": "Task",
                "priority": "Medium"
            }
        )
        print("Issue created successfully!")
        print(resp)
        
async def main():
    MCP_SERVER_URL = "http://127.0.0.1:3333/mcp"
    await Create_issue(MCP_SERVER_URL)
if __name__ == "__main__":
    asyncio.run(main())