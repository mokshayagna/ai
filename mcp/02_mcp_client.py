# src/35-MCP-Helloworld/02-mcpc.py
import asyncio
from fastmcp import Client

SERVER_URL = "http://127.0.0.1:3333/mcp/"
client = Client(SERVER_URL)

async def main():
    async with client:
        print(f"Client connected: {client.is_connected()}")

        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"{tool.model_dump_json(indent=4)}")

        if any(tool.name == "add_numbers" for tool in tools):
            result = await client.call_tool("add_numbers", {"a": 5, "b": 3})
            print(f"Result of add(5, 3): {result}")

if __name__ == "__main__":
    asyncio.run(main())
