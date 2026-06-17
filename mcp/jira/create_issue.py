import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def create_issue(server_url: str):

    async with AsyncExitStack() as stack:

        read_stream, write_stream, _ = (
            await stack.enter_async_context(
                streamablehttp_client(server_url)
            )
        )

        session = await stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await session.initialize()

        resp = await session.call_tool(
            "CREATE_ISSUE",
            {
                "project_key": "PROM",
                "summary": "MCP Test Issue",
                "description": "Created from MCP client",
                "issue_type": "Task"
                # Try without priority first
            }
        )

        print("\nFULL RESPONSE:\n")
        print(resp)

        print("\nCONTENT:\n")
        for item in resp.content:
            print(item.text)


async def main():

    MCP_SERVER_URL = "http://127.0.0.1:3333/mcp"

    await create_issue(
        MCP_SERVER_URL
    )


if __name__ == "__main__":
    asyncio.run(main())