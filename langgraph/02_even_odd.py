from langgraph.graph import StateGraph, START, END
from ig_utility import save_graph_as_png
from typing import TypedDict

class sate(TypedDict):
    n: int
    result: str
    
    
def is_even(state: sate) -> sate:
    
    if state["n"] % 2 == 0:
        return {"n": state["n"], "result": "even"}
    else:
        return {"n": state["n"], "result": "odd"}
    
def build_graph():
    
    builder = StateGraph(sate)
    
    builder.add_node("EVEN_OR_ODD", is_even)
    
    builder.add_edge(START, "EVEN_OR_ODD")
    builder.add_edge("EVEN_OR_ODD", END)
    
    graph = builder.compile()
    
    save_graph_as_png(graph, "02_even_odd_graph")
    
    return graph

graph = build_graph()
 
def main():
    
    data = {"n": 4}
    
    result = graph.invoke(data)
    print(f"result1: {result}")
    
    data = {"n": 9, "result": ""}
    result = graph.invoke(data)
    print(f"result2: {result}")
    print(f"result3: {result['result']}")
    
if __name__ == "__main__":
    main()