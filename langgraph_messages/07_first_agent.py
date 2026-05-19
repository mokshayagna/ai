from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from lg_utility import save_graph_as_png
from typing import TypedDict
from functools import partial
from langgraph.prebuilt import ToolNode, tools_condition

def add(a:int,b:int) -> int:
    """
    Add 'a' and 'b' and give the result.
    Args:
        a :int 
        b :int
    """
    retval = a + b
    return retval

def sub(a:int,b:int) -> int:
    """
    Subtract 'b' from 'a' and give the result.
    Args:
        a :int 
        b :int
    """
    retval = a - b
    return retval

def mul(a:int,b:int) -> int:
    """
    Multiply 'a' and 'b' and give the result.
    Args:
        a :int 
        b :int
    """
    retval = a * b
    return retval

def div(a:int,b:int) -> int:
    """
    Divide 'a' by 'b' and give the result.
    Args:
        a :int 
        b :int
    """
    retval = a / b
    return retval

def ask_llm(state:  MessagesState, llm):
    smsg = "You are an expert in mathetatics and performing arthematic operators"
    sys_msg = SystemMessage(content=smsg) 
    response = llm.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

def build_graph():
    builder = StateGraph(MessagesState)
    MODEL = "gemini-2.0-flash"
    llm = ChatGoogleGenerativeAI(model=MODEL)
    tools = [add, sub, mul, div]
    llm_with_tools = llm.bind_tools(tools)
    
    builder.add_node("ASK_LLM", partial(ask_llm, llm=llm_with_tools))
    builder.add_node("tools",ToolNode(tools=tools)) #creates automatic tool executor node.
    
    builder.add_edge(START, "ASK_LLM")
    builder.add_conditional_edges("ASK_LLM", tools_condition)
    builder.add_edge("tools", "ASK_LLM")
    builder.add_edge("ASK_LLM", END)
    
    graph = builder.compile()
    
    save_graph_as_png(graph, __file__)
    
    return graph

graph = build_graph()

def main():
    data = "ADD 5 and 3. Multiply with 2 and divide by 4. What is the result?"
    hmsg = HumanMessage(content=data)
    result = graph.invoke({"messages": [hmsg]})
    
    for msg in result["messages"]:
        msg.pretty_print()
        
if __name__ == "__main__":
    main()
           
    