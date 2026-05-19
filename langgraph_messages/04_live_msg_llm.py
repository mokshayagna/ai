from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage
from lg_utility import save_graph_as_png
from langchain_google_genai import ChatGoogleGenerativeAI
from functools import partial

def reply_node(state: MessagesState, llm):
    """
       this function will be called when we are in the ASSISTANT node, 
       and it will receive the current state of the messages, and it will use the llm to generate a new message 
       based on the current messages, and then it will return the new state with the new message added to the list of messages.
    """
    messages = state["messages"]

    new_message = llm.invoke(messages)

    return {"messages": messages + [new_message]}

def build_graph():
    MODEL = "gemini-2.0-flash"
    llm = ChatGoogleGenerativeAI(model=MODEL) 

    builder = StateGraph(MessagesState)
    builder.add_node("ASSISTANT", partial(reply_node, llm=llm))

    builder.add_edge(START, "ASSISTANT")
    builder.add_edge("ASSISTANT", END)
    
    graph = builder.compile()

    save_graph_as_png(graph, __file__)

    return graph

graph = build_graph()

def main():
    prompt1 = "Who is the Prime Minister of India?"
    hmsg = HumanMessage(content=prompt1)
    initial_state = {"messages": [hmsg]}
    result = graph.invoke(initial_state)

    prompt2 = "When was he elected?"
    hmsg2 = HumanMessage(content=prompt2)
    initial_state2 = {"messages": result["messages"] + [hmsg2]}
    result = graph.invoke(initial_state2)
    
    prompt3 = "IS 5 even number?"
    hmsg3 = HumanMessage(content=prompt3)
    initial_state3 = {"messages": result["messages"] + [hmsg3]}
    result = graph.invoke(initial_state3)
    print(f"result :\n{result}")
    for msg in result["messages"]:
        # print(f"{type(msg).__name__}: {msg.content}")
        msg.pretty_print()

if __name__ == "__main__":
    main()
