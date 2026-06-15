import asyncio
import os

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():

    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "ghcr.io/github/github-mcp-server"
        ],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN":
                os.getenv("GITHUB_TOKEN")
        }
    )
    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(read_stream,write_stream) as session:

            await session.initialize()

            result = await session.list_tools()
            
            print("\nAvailable Tools:\n")
            
            for tool in result.tools:
                print(tool.name)

if __name__ == "__main__":
    asyncio.run(main())