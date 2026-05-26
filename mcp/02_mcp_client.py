# src/35-MCP-Helloworld/02-mcpc.py
import asyncio
from fastmcp import Client

SERVER_URL = "http://127.0.0.1:3333/mcp/"
client = Client(SERVER_URL) # connect to the MCP server

async def main():
    async with client:  # connects to client and disconnect automatically 
        print(f"Client connected: {client.is_connected()}")

        tools = await client.list_tools() # Request the server for available tools and wait until the response arrives.
        print("Available tools:")
        for tool in tools:
            print(f"{tool.model_dump_json(indent=4)}")

        if any(tool.name == "add_numbers" for tool in tools):
            result = await client.call_tool("add_numbers", {"a": 5, "b": 3}) # call the tool and wait for the response of the tool.
            print(f"Result of add(5, 3): {result}")

if __name__ == "__main__":
    asyncio.run(main()) # Start the server and run the main function asynchronously.