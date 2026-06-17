import asyncio
from contextlib import AsyncExitStack
from functools import partial

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools

from lg_utilities import save_graph_as_png


# -----------------------------
# STATE
# -----------------------------

class State(MessagesState):
    route: str


# -----------------------------
# MCP
# -----------------------------

async def connect_mcp(server_url: str):
    stack = AsyncExitStack()

    read_stream, write_stream, _ = (
        await stack.enter_async_context(
            streamablehttp_client(server_url)
        )
    )

    session = await stack.enter_async_context(
        ClientSession(read_stream, write_stream)
    )

    await session.initialize()

    return session, stack


async def available_tools(session):
    return await load_mcp_tools(session)


# -----------------------------
# CONNECT NODE
# -----------------------------

async def connect_mcp_node(state):
    
    return{
        "route": "connected"
    }


def route_node(state):

    return state["route"]


# -----------------------------
# LLM
# -----------------------------

async def ask_llm(state: State, llm):

    system_prompt = """
    You are a Jira Assistant.

    Always use tools when the user asks to:
    - create issue
    - search issue
    - get issue
    - update issue
    - add comment
    - transition issue
    """

    response = await llm.ainvoke(
        [SystemMessage(content=system_prompt)]
        + state["messages"]
    )

    return {
        "messages": [response]
    }


# -----------------------------
# GRAPH
# -----------------------------

async def build_graph(session):

    tools = await available_tools(session)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        project="genai-432214",
        location="us-central1",
    )

    llm_with_tools = llm.bind_tools(tools)

    builder = StateGraph(State)

    builder.add_node("CONNECT_MCP",connect_mcp_node)

    builder.add_node("ASK_LLM",partial(ask_llm,llm=llm_with_tools))

    builder.add_node("tools",ToolNode(tools))

    # START -> CONNECT_MCP

    builder.add_edge(START, "CONNECT_MCP")

    # CONNECT_MCP -> ASK_LLM or END

    builder.add_conditional_edges("CONNECT_MCP",
        route_node,
        {
            "connected": "ASK_LLM",
            "not_connected": END
        }
    )

    # ASK_LLM -> tools or END

    builder.add_conditional_edges("ASK_LLM",tools_condition)

    # tools -> ASK_LLM

    builder.add_edge("tools","ASK_LLM")

    graph = builder.compile()

    save_graph_as_png(graph, __file__)

    return graph


# -----------------------------
# MAIN
# -----------------------------

async def main():

    server_url = "http://127.0.0.1:3333/mcp"

    session, stack = await connect_mcp(
        server_url
    )

    async with stack:

        graph = await build_graph(
            session
        )

        result = await graph.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content="""
                        Create a Jira issue.

                        Project: PROM
                        Summary: LangGraph Test3
                        Description: This issue was created from LangGraph.
                        Issue Type: Task
                        Priority: Medium
                        """
                    )   
                ]
            }
        )

        print("\nRESULT:\n")

        for msg in result["messages"]:
            msg.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())