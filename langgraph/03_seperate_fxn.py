from langgraph.graph import StateGraph, START, END
from ig_utility import save_graph_as_png
from typing import TypedDict

class sate(TypedDict):
    n: int
    result: str
    
def is_even(state: sate) -> sate:
    if state["n"] % 2 == 0:
        return {"n": state["n"], "result": "even"}

def is_odd(state: sate) -> sate:
    if state["n"] % 2 != 0:
        return {"n": state["n"], "result": "odd"}
    
def build_graph():
    builder = StateGraph(sate)
    
    builder.add_node("IS_EVEN", is_even)
    builder.add_node("IS_ODD", is_odd)
    
    builder.add_edge(START, "IS_EVEN")
    builder.add_edge("IS_EVEN", "IS_ODD")
    
    builder.add_edge("IS_ODD", END)
    
    graph = builder.compile()
    
    save_graph_as_png(graph, "03_seperate_odd_graph")
    
    return graph
def main():
    data = {"n":9}
    graph = build_graph()
    result = graph.invoke(data)
    print(f"result1: {result}")

if __name__ == "__main__":  
    main()
