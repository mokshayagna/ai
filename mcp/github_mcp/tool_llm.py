from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from functools import partial
from lg_utilities import save_graph_as_png

import asyncio
import os

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def available_tools(session):
    tools = await load_mcp_tools(session)
    return tools


async def ask_llm(state: MessagesState, llm):
    system_prompt = """
You are a GitHub MCP assistant.

When a user asks to:
- create files
- update files
- delete files
- read repository content
- create pull requests
- create issues

ALWAYS use the appropriate GitHub tool.

Do not explain which tool you would use.

Execute the tool directly.

After the tool completes,
summarize the result for the user.
"""
    response = await llm.ainvoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response]}

async def build_graph(session):

    tools = await available_tools(session)

    builder = StateGraph(MessagesState)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        project="genai-432214",
        location="us-central1",
    )

    llm_with_tools = llm.bind_tools(tools)

    builder.add_node("ASK_LLM", partial(ask_llm, llm=llm_with_tools))
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "ASK_LLM")
    builder.add_conditional_edges("ASK_LLM", tools_condition)
    builder.add_edge("tools", "ASK_LLM")

    graph = builder.compile()

    save_graph_as_png(graph, __file__)

    return graph


async def main():

    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run", "-i", "--rm",
            "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
            "ghcr.io/github/github-mcp-server"
        ],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")}
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            graph = await build_graph(session)

            prompt = """
Create a new file in the GitHub repository mokshayagna/ai.

File details:
- Path: mcp/github_mcp/just_test.py
- Content:
# just_test.py

Commit this file directly to the default branch.

After completing, return:
- The file path
- The commit SHA
- The file URL
"""

            result = await graph.ainvoke({
                "messages": [HumanMessage(content=prompt)]
            })

            for msg in result["messages"]:
                msg.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())