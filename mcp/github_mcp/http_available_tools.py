import asyncio
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

        result = await session.list_tools()
        print(f"\nAvailable Tools ({len(result.tools)}):")
        for tool in result.tools:
            print(f"  - {tool.name}")

if __name__ == "__main__":
    asyncio.run(main())