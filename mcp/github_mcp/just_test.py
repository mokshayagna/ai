import asyncio
import base64
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    async with AsyncExitStack() as stack:
        r, w, _ = await stack.enter_async_context(
            streamablehttp_client("http://127.0.0.1:8000/mcp")
        )
        session = await stack.enter_async_context(ClientSession(r, w))
        await session.initialize()

        content = base64.b64encode(b'print("moksha")').decode("utf-8")

        resp = await session.call_tool("create_or_update_file", {
            "kwargs": {
                "owner": "mokshayagna",
                "repo": "ai",
                "path": "mcp/github_mcp/test2.py",
                "message": "Add test.py",
                "content": content,
                "branch": "main"
            }
        })
        print(resp.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())