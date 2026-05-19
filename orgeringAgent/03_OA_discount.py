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

from amazon import amazon_item_with_discount
from flipkart import flipkart_item_with_discount
from meesho import meesho_item_with_discount


def ordering_agent(state: MessagesState, llm):
    
    msg = """You are a shopping assistant. Your task is to help the user find the item they want to purchase
    and quantity required,
    if they mention the platform then check the available quantity across that platform 
    and also provide the price after discount if applicable,
    if the platform is not mentioned check the available quantity across different platforms (Amazon, Flipkart, Meesho) 
    and also provide the price after discount if applicable.
    Finally, suggest the best option to the user based on price and availability."""
    
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
        flipkart_quantity_tool, amazon_quantity_tool, meesho_quantity_tool,
        amazon_item_with_discount, flipkart_item_with_discount, meesho_item_with_discount
    ]
    
    llm_with_tools = llm.bind_tools(tools)
    
    builder.add_node("ordering_agent", partial(ordering_agent, llm=llm_with_tools))
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
        """I want to order 5, iphone 13 compare all the prices and quantity available 
        across amazon, flipkart and meesho and suggest the best option to order from"""
    )
    hmsg = HumanMessage(content=msg)
    init_msg = {"messages": [hmsg]}
    response = graph.invoke(init_msg)
    for m in response["messages"]:
        m.pretty_print()
if __name__ == "__main__":
    main()