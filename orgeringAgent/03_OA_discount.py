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
           """Objective:
                Help the user order the requested quantity of an item 
                at the lowest possible total cost, splitting across platforms if needed.
            Available Tools:
                - flipkart_item_id_tool, amazon_item_id_tool, meesho_item_id_tool: 
                            Retrieve item IDs based on item name.
                - flipkart_quantity_tool, amazon_quantity_tool, meesho_quantity_tool: 
                            Check available quantity for a given item ID.
                - amazon_item_with_discount, flipkart_item_with_discount, meesho_item_with_discount: 
                            Calculate discounted price for a given item ID and quantity.
            Instructions:
                Step 1: Extract item name, required quantity, and platform (if specified) from the user query.
                Step 2: Platform specified → query only that platform's tools for: item_id, available_quantity, discounted_price.
                        No platform specified → query ALL three platforms in parallel.
                Step 3: If item is unavailable on all queried platforms → reply: "This item is currently out of stock on all platforms."
                        If item is available → proceed to step 4.
                        
                Step 4: • If ONE platform has enough stock → suggest that platform with its discounted price and total cost.
                        • If NO single platform has enough stock → split the order greedily by lowest unit price:
                            a. Sort platforms by discounted_price (ascending).
                            b. Allocate as many units as possible from the cheapest platform.
                            c. Fill the remainder from the next cheapest, and so on.
                            d. Present the split plan and the combined total cost.
                    
                Step 5: Present a clear, concise summary table:
                        Platform | Unit Price | Qty to Order | Subtotal
                        And state: "Best combined price for [qty] units: ₹[total]"
            Output Format:
                Always show prices in ₹ (INR).
                - If splitting across platforms, explain why (stock limits).
                - If one platform is cheapest and fully stocked, recommend it directly.
                - Keep the response concise — one table + one recommendation line.   
                Example Response:
                "The item is not available in the required quantity on a single platform, but here’s the best way to split your order:
                        Platform   | Unit Price | Qty to Order | Subtotal
                        ------------------------------------------------    
                give me answer for iphone 13 with quantity 12 compare all platforms
            
            """
    )
    Hmsg = (
        """query: I want to order 12 an iphone 13 from the e-commerce platforms,
        
        
        Tools to use: flipkart_item_id_tool, amazon_item_id_tool, meesho_item_id_tool,
        flipkart_quantity_tool, amazon_quantity_tool, meesho_quantity_tool,
        amazon_item_with_discount, flipkart_item_with_discount, meesho_item_with_discount 
        
        Instructions:
        1. Identify the item name and platform from the user query if provided.
        
        2. If platform is mentioned then use respective platform and extract item_id, available_quantity 
        and discounted price using the respective tools. 
        
        3. If platform is not mentioned then extract item_id, available_quantity and discounted price 
        across all platforms using the respective tools.
        
        4. If the required quantity is more than the available quantity then suggest the user about the available 
        quantity and discounted price across different platforms and suggest the best option based on the cheapest price and availability.
        example: if i asked for quantity of 12 then based on the low price divide the required quantity across different platforms 
        and suggest the best option to the user, The final price should be best low price all platform combined 
        
        5.If item is not available across all platforms then suggest the user that the item is out of stock.
        """
   )
    hmsg = HumanMessage(content=msg)
    init_msg = {"messages": [hmsg]}
    response = graph.invoke(init_msg)
    for m in response["messages"]:
        m.pretty_print()
if __name__ == "__main__":
    
    main()