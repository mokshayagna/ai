from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from functools import partial
from lg_utilities import save_graph_as_png

import asyncio
import os

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def available_tools():

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
                os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
        }
    )

    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            tool_info = []

            for tool in tools.tools:
                tool_info.append(
                    {
                        "name": tool.name,
                        "description": tool.description
                    }
                )

            return tool_info


async def ask_llm(state: MessagesState, llm, tools):

    tool_text = ""

    for tool in tools:
        tool_text += (
            f"Tool Name: {tool['name']}\n"
            f"Description: {tool['description']}\n\n"
        )

    smsg = f"""
        You are a GitHub MCP assistant.

        Available tools:

        {tool_text}

        The user will ask a question.

        Your task:
        1. Identify the best tool.
        2. Explain why.
        3. Return the tool name and reason.
        """

    sys_msg = SystemMessage(content=smsg)

    response = llm.invoke(
        [sys_msg] + state["messages"]
    )

    return {"messages": [response]}


async def build_graph():

    tools = await available_tools()

    builder = StateGraph(MessagesState)

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.7
    )

    builder.add_node(
        "ASK_LLM",
        partial(
            ask_llm,
            llm=llm,
            tools=tools
        )
    )

    builder.add_edge(START, "ASK_LLM")
    builder.add_edge("ASK_LLM", END)

    graph = builder.compile()

    save_graph_as_png(graph, __file__)

    return graph


async def main():

    graph = await build_graph()

    prompt = "Which tool should I use to create a file?"

    result = await graph.ainvoke(
        {
            "messages": [
                HumanMessage(content=prompt)
            ]
        }
    )

    for msg in result["messages"]:
        msg.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())