from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from lg_utility import save_graph_as_png
from typing import TypedDict
from functools import partial

class State(TypedDict):
    input : str
    response : str
    route : str
    
def ask_llm_node(state: State, llm):
    input = state["input"]
    response = llm.invoke(input)
    state["response"] = response.content
    return state

def error_node(state: State):
    state["response"] = "Sorry, I can't answer this question"
    return state

def route_node(state: State):
    retval = state["route"]
    return retval

def validator_node(state: State):
    input = state["input"]
    if "capital" in input.lower():
        state["route"] = "capital"
    else:
        state["route"] = "error"
    return state

def build_graph():
    builder = StateGraph(State)
    MODEL = "gemini-2.0-flash"
    llm = ChatGoogleGenerativeAI(model=MODEL)
    
    builder.add_node("VALIDATOR", validator_node)
    builder.add_node("ASK_LLM", partial(ask_llm_node, llm=llm))
    builder.add_node("ERROR", error_node)
    
    builder.add_edge(START, "VALIDATOR")
    builder.add_conditional_edges(
        "VALIDATOR",
        route_node,
        {
            "capital": "ASK_LLM",
            "error": "ERROR"
        },
    )
    
    builder.add_edge("ASK_LLM", END)
    builder.add_edge("ERROR", END)
    
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
    
    data2 = {
        "input": "Who is the PM of India?",
        "response": ""
    }   
    result2 = graph.invoke(data2)
    print(f"result2 :\n{result2}")
if __name__ == "__main__":
    main()