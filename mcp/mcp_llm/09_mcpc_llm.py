import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from langchain_mcp_adapters.tools import load_mcp_tools

async def main():
    server_url = "http://127.0.0.1:3333/mcp/"
    MODEL = "gemini-2.0-flash"

    llm = ChatGoogleGenerativeAI(model = MODEL)

    client_ctx = streamablehttp_client(server_url)
    r,w,_ = await client_ctx.__aenter__()

    session = ClientSession(r,w)
    await session.__aenter__()
    await session.initialize()

    tools = await load_mcp_tools(session)
    llm_with_tools = llm.bind_tools(tools)

    prompt = "add 5 and 10"
    hmsg = HumanMessage(content = prompt)

    print(f"Sending prompt to LLM: {prompt}")
    response  = llm_with_tools.invoke([hmsg])
    print("Type of response:", type(response))
    print(f"LLM response: {response.tool_calls}")
    
    for tool in response.tool_calls:
        tool_name =tool["name"]
        tool_args = tool["args"]
        print(f"LLM requested tool:{tool_name}with arguments{tool_args}")
        result = await session.call_tool(tool_name,tool_args)
        print(f"Tool result:{result.content[0].text}")

    await session.__aexit__(None, None, None)
    await client_ctx.__aexit__(None, None, None)

if __name__ == "__main__":
    asyncio.run(main())