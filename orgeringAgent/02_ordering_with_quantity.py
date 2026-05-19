from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from functools import partial
from lg_utilities import save_graph_as_png

from amazon import amazon_item_id_tool
from flipkart import flipkart_item_id_tool
from meesho import meesho_item_id_tool

from amazon import amazon_quantity_tool
from flipkart import flipkart_quantity_tool
from meesho import meesho_quantity_tool

def orgering_agent(state: MessagesState, llm):
    
    msg = """You are a shopping assistant. Your task is to help the user find the item 
    they want to purchase from mentioned platform, if not mentioned check the available quantity across different platforms (Amazon, Flipkart, Meesho)."""
    
    sys_msg = SystemMessage(content=msg)
    prompt = [sys_msg] + state['messages']
    
    response = llm.invoke(prompt)
    return {'messages': [response]}

def build_graph():
    builder = StateGraph(MessagesState)
    MODEL = "gemini-2.0-flash"
    llm = ChatGoogleGenerativeAI(model=MODEL)
    
    tools = [
        flipkart_item_id_tool, amazon_item_id_tool, meesho_item_id_tool,
        flipkart_quantity_tool, amazon_quantity_tool, meesho_quantity_tool
    ]
    
    llm_with_tools = llm.bind_tools(tools)
    
    builder.add_node("ordering_agent", partial(orgering_agent, llm=llm_with_tools))
    builder.add_node("tools", ToolNode(tools=tools))
    
    builder.add_edge(START, "ordering_agent")
    builder.add_conditional_edges("ordering_agent", tools_condition)
    builder.add_edge("tools", "ordering_agent")
    builder.add_edge("ordering_agent", END)
    
    graph = builder.compile()
    save_graph_as_png(graph, __file__)
    return graph

graph = build_graph()

def main():
    msg = (
        "I want to order 12, iphone 13"
        "from meesho"
    )
    hmsg = HumanMessage(content=msg)
    init_msg = {"messages": [hmsg]}
    response = graph.invoke(init_msg)
    
    for m in response["messages"]:
        m.pretty_print()

if __name__ == "__main__":
    main()
    