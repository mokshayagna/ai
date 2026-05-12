from langgraph.graph import START, END, StateGraph
from ig_utility import save_graph_as_png
from typing import TypedDict


class State(TypedDict):
    attempts: int
    status: str
    route: str
    msg: str


def initialize(state: dict):

    return {
        "attempts": 0,
        "status": "",
        "route": "",
        "msg": ""
    }


def send_email(state: State):

    state["attempts"] += 1

    print(
        f"Trying attempt "
        f"{state['attempts']}"
    )

    if state["attempts"] == 4:

        state["status"] = "success"
        state["route"] = "success"

        print("E-mail sent successfully")

    else:

        state["status"] = "fail"
        state["route"] = "fail"

        print("E-mail sending failed")

    return state


def success(state: State):

    state["msg"] = (
        f"E-mail sent successfully at "
        f"attempt {state['attempts']}"
    )

    return state


def fail(state: State):

    if state["attempts"] >= 3:

        state["msg"] = (
            "E-mail didn't send. "
            "Maximum attempts exceeded."
        )

        state["route"] = "stop"

    else:

        state["msg"] = (
            f"E-mail failed at "
            f"attempt {state['attempts']}. "
            f"Retrying..."
        )

        state["route"] = "retry"

    return state


def retry_decide(state: State):

    return state["route"]


def build_graph():

    builder = StateGraph(State)

    builder.add_node("INITIALIZE", initialize)
    
    builder.add_node("SEND_EMAIL",send_email)

    builder.add_node("SUCCESS",success)

    builder.add_node("FAIL",fail)

    builder.add_edge(START,"INITIALIZE")

    builder.add_edge("INITIALIZE","SEND_EMAIL")

    builder.add_conditional_edges(
        "SEND_EMAIL",
        retry_decide,
        {
            "success": "SUCCESS",
            "fail": "FAIL"
        }
    )

    builder.add_conditional_edges(
        "FAIL",
        retry_decide,
        {
            "retry": "SEND_EMAIL",
            "stop": END
        }
    )

    builder.add_edge("SUCCESS",END)

    graph = builder.compile()

    save_graph_as_png( graph,__file__)

    return graph


graph = build_graph()


def main():

    response = graph.invoke({})

    print("\nFinal Message:")

    print(response["msg"])


if __name__ == "__main__":

    main()