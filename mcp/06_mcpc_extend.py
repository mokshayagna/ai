from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio

SERVER_URL = "http://127.0.0.1:3333/mcp/"

async def main():
        async with streamablehttp_client(SERVER_URL) as (read,write,_):  # connects to client and disconnect automatically 
            async with ClientSession(read,write) as session: # creates a client session for making requests to the server
                await session.initialize() # initializes the session by fetching the server's prompts, resources, and tools
                print(f"Client connected:")
            
                response = await session.list_prompts() # Request the server for available prompts and wait until the response arrives. 
                print("Available prompts:")
                for prompt in response:
                    print(prompt)
                
                response = await session.list_resources() # Request the server for available resources and wait until the response arrives.
                print("Available resources:")
                for resource in response:
                    print(resource)
                    
                response = await session.list_tools() # Request the server for available tools and wait until the response arrive      
                print("Available tools:")
                for tool in response:
                    print(tool)
                
                prompt_name = "example_prompt"
                prompt_args = {"question": "What is 2 + 3?"}
                print(f"Calling prompt '{prompt_name}' with arguments: {prompt_args}")
                response = await session.get_prompt(prompt_name, prompt_args) # call the prompt and wait for the response of the prompt.
                print(response.messages[0].content.text) # print the content of the first message in the response.
                
                resource_name = "greeting"
                args = "PromptlyAI"
                print(f"Get Resource of type :'{resource_name}' with args :{args}")
                content, mime_type = await session.read_resource(f"{resource_name}://{args}")
                print(mime_type[1][0].text)
                
                tool_name = "add_numbers"
                tool_args = {"a": 5, "b": 3}
                print(f"Calling tool '{tool_name}' with arguments: {tool_args}")
                response = await session.call_tool(tool_name, tool_args) # call the tool and wait for the response of the tool.
                print(response.content[0].text) # print the content of the first message in the response.
                
if __name__ == "__main__":
    asyncio.run(main()) # Start the server and run the main function asynchronously.