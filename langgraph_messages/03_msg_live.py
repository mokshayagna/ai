from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage
from lg_utility import save_graph_as_png

def reply_node(state:MessagesState):
    """
    class MessagesState(TypedDict):
       messages: List[]
       internally we will maintain a list of messages in the state, and each node can read the messages and add new messages to the list.
    """
    messages = state["messages"] # This is inbuilt in the state.
    new_msg = AIMessage(content="Narendra Modi") # We explicitly generate answer.
    return {"messages": messages + [new_msg]}  # We return the new state with the new message added to the list of messages.

def build_graph():
    builder = StateGraph(MessagesState)
    
    builder.add_node("ASSISSTANT",reply_node)
    builder.add_edge(START,"ASSISSTANT")
    builder.add_edge("ASSISSTANT",END)
    
    graph = builder.compile()
    
    save_graph_as_png(graph, __file__)
    
    return graph

graph = build_graph()   

def main():
    prompt = "who is PM of INDIA?"
    msg = HumanMessage(content= prompt)
    intial_stage =  {"messages":[msg]}
    response = graph.invoke(intial_stage)
    
    prompt2 = "when was he elected?"
    msg2 = HumanMessage(content= prompt2)
    intial_stage2 =  {"messages":response["messages"] + [msg2]}
    response = graph.invoke(intial_stage2)
    
    print(f"response: {response}")
    
    for msg in response["messages"]:
        # print(f"{type(msg).__name__}: {msg.content}")
        msg.pretty_print()
        
if __name__ == "__main__":
    main()
