import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    async with streamablehttp_client(
        "http://127.0.0.1:3333/mcp"
    ) as (read_stream, write_stream, _):

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "SEARCH_ISSUES",
                {
                    "jql": "project = PROM",
                    "max_results": 5
                }
            )

            print(result)

asyncio.run(main())