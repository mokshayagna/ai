from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from lg_utility import save_graph_as_png
from typing import TypedDict
from functools import partial

class MessagesState(TypedDict):
    input : str
    response : str
    
def reply_node(state: MessagesState, llm):
    """
    this function will be called when we are in the ASSISTANT node,
    and it will receive the current state of the messages, and it will use the llm to generate a new message
    based on the current messages, and then it will return the new state with the new message added to the list of messages.
    """
    input = state["input"]
    response = llm.invoke(input)
    state["response"] = response.content
    return state

def build_graph():
    builder = StateGraph(MessagesState)
    MODEL = "gemini-2.0-flash"
    llm = ChatGoogleGenerativeAI(model=MODEL)
    builder.add_node("ASSISTANT", partial(reply_node, llm=llm))
    builder.add_edge(START, "ASSISTANT")
    builder.add_edge("ASSISTANT", END)
    
    graph = builder.compile()
    save_graph_as_png(graph, __file__)
    return graph

graph = build_graph()

def main():
    data = {
        "input": "What is the capital of India?",
        "response": ""
    }
    
    result = graph.invoke(data)
    print(f"result :\n{result}")
    
if __name__ == "__main__":
    main()
