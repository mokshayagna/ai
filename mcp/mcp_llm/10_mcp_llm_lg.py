from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from lg_utility import save_graph_as_png
from functools import partial

from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools

async def ask_llm(state:MessagesState,llm_tools):
    smsg = "You are an expert in Mathematics and perform arthemetic operations"
    sys_msg = SystemMessage(content=smsg)
    
    response = llm_tools.invoke([sys_msg] + state["messages"])
    
    return{f"messages": [response]}

async def build_graph(session):
    builder = StateGraph(MessagesState)
    MODEL = "gemini-2.0-flash"
    llm = ChatGoogleGenerativeAI(model = MODEL)
    
    tools = await load_mcp_tools(session)
    llm_with_tools = llm.bind_tools(tools)
    
    builder.add_node("ASK_LLM",partial(ask_llm,llm_tools = llm_with_tools))
    builder.add_node("tools",ToolNode(tools))
    
    builder.add_edge(START,"ASK_LLM")
    builder.add_conditional_edges("ASK_LLM",tools_condition)
    builder.add_edge("tools","ASK_LLM")
    
    graph = builder.compile()
    
    #save_graph_as_png(graph,__file__)
    
    return graph

async def main():
    SERVER_URL = "http://127.0.0.1:3333/mcp/"
    async with streamablehttp_client(SERVER_URL) as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()
            
            react_graph = await build_graph(session)
            
            prompt = "add 10 and 20"
            hmsg = HumanMessage(content=prompt)
            messages = [hmsg]
            print(f"Agent->Prompting Model : {prompt}")
            
            response = await react_graph.ainvoke({"messages": messages})
            
            print("Agent->Final Response:")

            for msg in response["messages"]:
                if isinstance(msg, AIMessage):
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tool in msg.tool_calls:
                            print(
                                f"\tTool Called : "
                                f"{tool['name']} "
                                f"Args : "
                                f"{tool['args']}"
                            )
                    if msg.content:
                        print(
                            f"\tModel Response : "
                            f"{msg.content}"
                        )
if __name__ == "__main__":
    asyncio.run(main())
