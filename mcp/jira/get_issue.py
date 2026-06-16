import os
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def get_issue(server_url: str, issue_key: str):
    async with AsyncExitStack() as stack:
        r, w, _ = await stack.enter_async_context(streamablehttp_client(server_url))
        session = await stack.enter_async_context(ClientSession(r, w))
        await session.initialize()

        resp = await session.call_tool("GET_ISSUE", {"issue_key": issue_key})
        print(resp.content[0].text)

if __name__ == "__main__":
    SERVER_URL = os.getenv("MCP_SERVER_URL") or "http://127.0.0.1:3333/mcp"
    asyncio.run(get_issue(SERVER_URL, "PROM-6"))