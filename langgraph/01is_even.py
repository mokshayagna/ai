from langgraph.graph import StateGraph, START, END
from ig_utility import save_graph_as_png
from typing import TypedDict


class State(TypedDict):
    n: int

def is_even(state: State) -> State:

    print(f"state: {state}")

    if state["n"] % 2 == 0:
        print({"n": state["n"], "result": "even"})

    else:
        print({"n": state["n"], "result": "odd"})

    return state


def build_graph():

    builder = StateGraph(State)

    builder.add_node("EVEN_OR_ODD", is_even)

    builder.add_edge(START, "EVEN_OR_ODD")
    builder.add_edge("EVEN_OR_ODD", END)

    graph = builder.compile()

    save_graph_as_png(graph, "is_even_graph")

    return graph

graph = build_graph()

def main():

    data = {"n": 4}

    result = graph.invoke(data)

    print(f"result: {result}")

if __name__ == "__main__":
    main()