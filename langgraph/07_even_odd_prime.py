from langgraph.graph import START, END, StateGraph
from ig_utility import save_graph_as_png
from typing import TypedDict

class State(TypedDict):
    n : int
    result : str
    route : str
    
def is_even_odd(State : State) -> State:
    if State['n'] % 2 == 0:
        return {"n":State["n"], "result":"Even"}
    else:
        return {"n":State["n"], "result":"Odd"}

def is_prime(State):
    n = State['n']
    if n <= 1:
        print(f"{n} is not prime")
    else:
        is_prime = True
        
        for i in range(2,n):
            if n%i == 0:
                is_prime = False
                break
        if is_prime:
            print(f"{n} is prime")
        else:
            print(f"{n} is not prime")

def route_decide(state:State):
    
    retval = state["route"]
    return retval

def build_graph():
    builder = StateGraph(State)
    
    builder.add_node("EVEN_ODD",is_even_odd)
    builder.add_node("PRIME",is_prime)
    
    builder.add_edge(START,"EVEN_ODD")
    
    builder.add_conditional_edges(
        "EVEN_ODD",
        route_decide,
        {
            "Odd": "PRIME",
            "Even": END
        }
    )
    
    builder.add_edge("EVEN_ODD","END")
    builder.add_edge("PRIME","END")
    
    graph = builder.compile()
    save_graph_as_png(graph, __file__)

    return graph


graph = build_graph()
def main():

    response = graph.invoke({"n": 4})
    print(f"Number: {response['n']}, Result: {response['result']}")
    
    response = graph.invoke({"n": 5})
    print(f"Number: {response['n']}, Result: {response['result']}")


if __name__ == "__main__":
    main()
    
    
    