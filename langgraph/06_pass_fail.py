from langgraph.graph import START, StateGraph, END
from ig_utility import save_graph_as_png
from typing import TypedDict


class State(TypedDict):
    marks: int
    route: str
    status: str


def Evaluate(state: State):

    if state["marks"] > 40:
        state["route"] = "pass"

    else:
        state["route"] = "fail"

    return state


def route_decide(state: State):

    retval = state["route"]

    return retval


def node_pass(state: State):

    state["status"] = "PASS"

    return state


def node_fail(state: State):

    state["status"] = "FAIL"

    return state


def build_graph():

    builder = StateGraph(State)

    builder.add_node("EVALUATOR", Evaluate)
    builder.add_node("FAIL", node_fail)
    builder.add_node("PASS", node_pass)

    builder.add_edge(START, "EVALUATOR")

    builder.add_conditional_edges(
        "EVALUATOR",
        route_decide,
        {
            "pass": "PASS",
            "fail": "FAIL"
        }
    )

    builder.add_edge("PASS", END)
    builder.add_edge("FAIL", END)

    graph = builder.compile()

    save_graph_as_png(graph, __file__)

    return graph


graph = build_graph()


def main():

    response = graph.invoke({"marks": 45})

    print(f"Marks: {response['marks']}, Status: {response['status']}")

    response = graph.invoke({"marks": 30})

    print(f"Marks: {response['marks']}, Status: {response['status']}")


if __name__ == "__main__":
    main()