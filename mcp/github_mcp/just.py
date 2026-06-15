import asyncio
from mcp.client.streamable_http import streamablehttp_client

async def main():
    async with streamablehttp_client(
        "http://localhost:8082/mcp"
    ) as streams:
        print(type(streams))
        print(streams)

asyncio.run(main())