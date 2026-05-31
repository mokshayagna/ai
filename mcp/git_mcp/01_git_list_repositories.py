import os
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def MCPS_List_Tools(server_url):

    async with AsyncExitStack() as stack:

        r,w,_ = await stack.enter_async_context(
            streamablehttp_client(server_url)
        )

        session = await stack.enter_async_context(
            ClientSession(r,w)
        )

        await session.initialize()

        resp = await session.list_tools()

        for t in resp.tools:
            print(t.name)


async def main():

    url="http://127.0.0.1:3333/mcp/"

    await MCPS_List_Tools(url)


asyncio.run(main())