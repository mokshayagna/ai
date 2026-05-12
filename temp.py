from typing import TypedDict

class State(TypedDict):
    quantity: int
    req_item: str
    items: dict
    availability: str

def stock(state: State):
    state["items"] = {
        "laptop": 10,
        "phone": 2,
        "headphones": 0
    }
    return state

def availability_check(state: State):

    items = state["items"]

    if state["req_item"] in items:

        available_quantity = items[state["req_item"]]

        print("Available quantity:", available_quantity)

        if available_quantity >= state["quantity"]:
            state["availability"] = "available"
        else:
            state["availability"] = "not available"

    return state
  
def main():
  response = {
    "quantity": 1,
    "req_item": "laptop"
  }
