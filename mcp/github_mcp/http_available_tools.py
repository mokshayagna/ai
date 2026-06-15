import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():

    async with streamablehttp_client(
        "http://localhost:8082/mcp"
    ) as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.list_tools()

            print("\nAvailable Tools:\n")

            for tool in result.tools:
                print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())