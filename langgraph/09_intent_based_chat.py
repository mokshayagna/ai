from langgraph.graph import START, END, StateGraph
from ig_utility import save_graph_as_png
from typing import TypedDict


class State(TypedDict):
    msg: str
    faq: list
    complaints: list
    talk: list
    route: str
    output: str


def initialize(state: dict):

    return {
        "msg": state.get("msg", ""),
        "faq": [],
        "complaints": [],
        "talk": [],
        "route": "",
        "output": ""
    }


def classify_intent(state: State):

    msg = state["msg"].lower()

    if "return" in msg or "refund" in msg:
        state["route"] = "complaint"

    elif "how can" in msg or "what is" in msg:
        state["route"] = "faq"

    else:
        state["route"] = "talk"

    return state


def handle_complaints(state: State):

    state["complaints"].append(
        "Your complaint has been registered"
    )

    return state


def handle_faq(state: State):

    state["faq"].append(
        "Here is the information you requested"
    )

    return state


def handle_talk(state: State):

    state["talk"].append(
        "Hi! How can I assist you today?"
    )

    return state


def route_decide(state: State):

    return state["route"]


def decision(state: State):

    if len(state["complaints"]):

        state["output"] = state["complaints"][-1]

    elif len(state["faq"]):

        state["output"] = state["faq"][-1]

    elif len(state["talk"]):

        state["output"] = state["talk"][-1]

    return state


def build_graph():

    builder = StateGraph(State)

    builder.add_node("INITIALIZE", initialize)

    builder.add_node("CLASSIFY_INTENT",classify_intent)

    builder.add_node("HANDLE_COMPLAINTS",handle_complaints)

    builder.add_node("HANDLE_FAQ",handle_faq)

    builder.add_node("HANDLE_TALK",handle_talk)

    builder.add_node("DECISION",decision)

    builder.add_edge(START, "INITIALIZE")

    builder.add_edge("INITIALIZE","CLASSIFY_INTENT")

    builder.add_conditional_edges(
        "CLASSIFY_INTENT",
        route_decide,
        {
            "complaint": "HANDLE_COMPLAINTS",
            "faq": "HANDLE_FAQ",
            "talk": "HANDLE_TALK"
        }
    )

    builder.add_edge("HANDLE_COMPLAINTS","DECISION")

    builder.add_edge("HANDLE_FAQ", "DECISION")

    builder.add_edge("HANDLE_TALK","DECISION")

    builder.add_edge("DECISION", END)

    graph = builder.compile()

    save_graph_as_png( graph,"09_intent_based_chat")

    return graph


graph = build_graph()


def main():

    input_msg = {"msg": "what is the time?"}
    response = graph.invoke(input_msg)
    print(f"Input: {input_msg['msg']}")
    print(f"Agent Response: {response['output']}")
    print()
    
    input_msg = {"msg": "refund the product"}
    response = graph.invoke(input_msg)
    print(f"Input: {input_msg['msg']}")
    print(f"Agent Response: {response['output']}")
    print()
    
    input_msg = { "msg":"hello"}
    response = graph.invoke(input_msg)
    print(f"Input: {input_msg['msg']}")
    print(f"Agent Response: {response['output']}")
    

if __name__ == "__main__":

    main()