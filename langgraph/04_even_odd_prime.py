from langgraph.graph import StateGraph, START, END
from ig_utility import save_graph_as_png
from typing import TypedDict

class state(TypedDict):
    n : int
    result: str
    
def is_even(state: state) -> state:
    if state["n"] % 2 == 0:
        return {"n": state["n"], "result": "even"}

def is_odd(state: state) -> state:
    if state["n"] % 2 != 0:
        return {"n": state["n"], "result": "odd"}

def prime(state):

    n = state["n"]

    if n <= 1:
        print(f"{n} is not prime")
    else:
        is_prime = True

        for i in range(2, n):

            if n % i == 0:
                is_prime = False
                break
        if is_prime:
            print(f"{n} is prime")

        else:
            print(f"{n} is not prime")

    return state
            
def build_graph():
    builder = StateGraph(state)
    
    builder.add_node("IS_EVEN", is_even)
    builder.add_node("IS_ODD", is_odd)
    builder.add_node("IS_PRIME", prime)
    
    builder.add_edge(START, "IS_PRIME")
    builder.add_edge("IS_PRIME", "IS_ODD")
    builder.add_edge("IS_PRIME", "IS_EVEN")
    
    builder.add_edge("IS_EVEN", END)
    builder.add_edge("IS_EVEN", END)
    
    
    graph = builder.compile()
    
    save_graph_as_png(graph, "04_even_odd_prime_graph")
    
    return graph

def main():
    data = {"n":9}
    graph = build_graph()
    result = graph.invoke(data)
    print(f"result1: {result}")
    
if __name__ == "__main__":
    main()