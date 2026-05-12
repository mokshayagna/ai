from langgraph.graph import START, END, StateGraph
from ig_utility import save_graph_as_png
from typing import TypedDict


class State(TypedDict):
    req_item: str
    quantity_req: int
    quantity_avbl: int
    route: str
    partial_stock_avbl: bool
    cost: int
    items: dict


def initialize(state: dict):

    return {
        "req_item": state.get("req_item", ""),
        "quantity_req": int(state.get("quantity_req", 0)),
        "quantity_avbl": 0,
        "route": "",
        "partial_stock_avbl": False,
        "cost": 0,
        "items": {}
    }


def stock(state: State):

    state["items"] = {
        "laptop": 10,
        "phone": 2,
        "headphones": 0
    }

    return state


def cost_per_item(state: State):

    cost_dict = {
        "laptop": 1000,
        "phone": 500,
        "headphones": 100
    }

    item = state["req_item"]

    if item in cost_dict:
        state["cost"] = cost_dict[item]

    return state


def add_cart(state: State):
    if state["quantity_req"] > 0 and state["quantity_avbl"] >= state["quantity_req"]: 
        print(
            f"{state['quantity_req']} {state['req_item']} added to cart."
        )
    else:
        print(
            f"Cannot add {state['quantity_req']} "
            f"{state['req_item']} to cart due to insufficient stock."
        )
    return state


def check_availability(state: State):

    req_item = state["req_item"]
    quantity_required = state["quantity_req"]

    items = state["items"]

    if req_item in items:

        quantity_available = items[req_item]

        if quantity_available == 0:

            state["route"] = "out of stock"

        elif quantity_available >= quantity_required:

            state["route"] = "available"

        else:

            state["route"] = "partial availability"
            state["quantity_avbl"] = quantity_available

    else:

        state["route"] = "out of stock"

    return state


def route_decide(state: State):

    return state["route"]


def partial_price_calculation(state: State):

    available_quantity = state["quantity_avbl"]

    total_cost = available_quantity * state["cost"]

    print(
        f"Only {available_quantity} units of "
        f"{state['req_item']} are available."
    )

    print(
        f"Total cost for available quantity: {total_cost}"
    )

    return state


def payment_successful():

    return True


def payment(state: State):

    if state["route"] == "available":

        if payment_successful():

            total_cost = (
                state["cost"] * state["quantity_req"]
            )

            print(
                f"Payment successful for "
                f"{state['req_item']}."
            )

            print(f"Total cost: {total_cost}")

        else:

            print(
                f"Payment failed for "
                f"{state['req_item']}."
            )

    elif state["route"] == "partial availability":

        print(
            f"Partial stock available for "
            f"{state['req_item']}."
        )

    else:

        print(
            f"Sorry, {state['req_item']} is out of stock."
        )

    return state


def confirm(state: State):

    if state["route"] == "available":

        print(
            f"Your order for "
            f"{state['req_item']} has been confirmed!"
        )

    return state


def build_graph():

    builder = StateGraph(State)

    builder.add_node("INITIALIZE", initialize)
    builder.add_node("STOCK", stock)
    builder.add_node("COST_PER_ITEM", cost_per_item)
    builder.add_node("ADD_CART", add_cart)
    builder.add_node("CHECK_AVAILABILITY", check_availability)
    builder.add_node(
        "PARTIAL_PRICE_CALCULATION",
        partial_price_calculation
    )
    builder.add_node("PAYMENT", payment)
    builder.add_node("CONFIRM", confirm)

    builder.add_edge(START, "INITIALIZE")

    builder.add_edge("INITIALIZE", "STOCK")

    builder.add_edge("STOCK", "COST_PER_ITEM")

    builder.add_edge("COST_PER_ITEM", "ADD_CART")

    builder.add_edge("ADD_CART", "CHECK_AVAILABILITY")

    builder.add_conditional_edges(
        "CHECK_AVAILABILITY",
        route_decide,
        {
            "available": "PAYMENT",
            "partial availability":
                "PARTIAL_PRICE_CALCULATION",
            "out of stock": "PAYMENT"
        }
    )

    builder.add_edge(
        "PARTIAL_PRICE_CALCULATION",
        "PAYMENT"
    )

    builder.add_edge("PAYMENT", "CONFIRM")

    builder.add_edge("CONFIRM", END)

    graph = builder.compile()

    save_graph_as_png(graph, __file__)

    return graph


graph = build_graph()


def main():

    input_data = {
        "req_item": "headphones",
        "quantity_req": 1
    }

    response = graph.invoke(input_data)

    print("\nFinal State:")
    print(response)


if __name__ == "__main__":
    main()