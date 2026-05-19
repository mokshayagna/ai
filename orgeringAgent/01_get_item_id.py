from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from functools import partial
from lg_utilities import save_graph_as_png


def flipkart_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Flipkart"""

    flipkart_items = {
        "iPhone 13": "FK12345",
        "Samsung Galaxy S21": "FK54321",
        "MacBook Pro": "FK67890"
    }

    for item in flipkart_items:
        if item.lower() == item_name.lower():
            return flipkart_items[item]

    return "Item not found"

def amazon_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Amazon"""

    amazon_items = {
        "iPhone 13": "AM12345",
        "Samsung Galaxy S21": "AM54321",
        "MacBook Pro": "AM67890"
    }

    for item in amazon_items:
        if item.lower() == item_name.lower():
            return amazon_items[item]

    return "Item not found"

def meesho_item_id_tool(item_name: str) -> str:
    """Retrieves item id from Meeshop"""

    meeshop_items = {
        "iPhone 13": "MS12345",
        "Samsung Galaxy S21": "MS54321",
        "MacBook Pro": "MS67890"
    }

    for item in meeshop_items:
        if item.lower() == item_name.lower():
            return meeshop_items[item]

    return "Item not found"
    
def ordering_agent(state: MessagesState, llm):

    sys_prompt = (
        "You are a helpful assistant tasked with retrieving item ids from various e-commerce platforms based on user queries. "
        "Use the provided tools to get the item id from the respective platform. "
        "If the user query does not specify a platform, use the flipkart_item_id_tool by default. "
        "Only use the tools when necessary and always provide a response to the user query, even if the item is not found. "
    )

    sys_msg = SystemMessage(content=sys_prompt)

    prompt = [sys_msg] + state["messages"]

    response = llm.invoke(prompt)

    return {"messages": [response]}


def build_graph():

    builder = StateGraph(MessagesState)

    llm = ChatGoogleGenerativeAI( model="gemini-2.0-flash")

    tools = [flipkart_item_id_tool,amazon_item_id_tool,meesho_item_id_tool]

    llm_with_tools = llm.bind_tools(tools)

    builder.add_node("ordering_agent",partial(ordering_agent, llm=llm_with_tools))

    builder.add_node("tools",ToolNode(tools=tools))

    builder.add_edge(START, "ordering_agent")

    builder.add_conditional_edges(
        "ordering_agent",
        tools_condition
    )

    builder.add_edge("tools", "ordering_agent")

    builder.add_edge("ordering_agent", END)

    graph = builder.compile()
    
    save_graph_as_png(graph, __file__)

    return graph

graph = build_graph()

def main():

    msg = (
        "I want to order an iphone 14 "
        "from meesho"
    )

    hmsg = HumanMessage(content=msg)
    
    init_msg = {"messages": [hmsg]}

    response = graph.invoke(init_msg)

    for m in response["messages"]:
        m.pretty_print()


if __name__ == "__main__":
    main()