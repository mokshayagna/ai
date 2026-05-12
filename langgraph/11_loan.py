from langgraph.graph import START,END,StateGraph
from ig_utility import save_graph_as_png
from typing import TypedDict

class State(TypedDict):
        age : int
        salary : int
        credit_score : int
        route : str
        loan_amount : int
        balance : int
        status : bool
        reason : str
        final_output: str
        salary:int

def intialize(state:State):
    return{
        "age" : state.get("age",0),
        "loan_amount" : state.get("loan_amount",0),
        "salary" : state.get("salary",0),
        "credit_score" : state.get("credit_score",0),
        "route" : "",
        "balance" : 50000,
        "status" : False,
        "reason" : "",
        "final_output" : ""
    }
def route_decide(state:State):
    retval = state["route"]
    return retval

def loan_amount_checking(state:State):
    req_amount = state["loan_amount"]
    if req_amount < state["balance"]:
        state["status"] = True
        state["route"] = "eligible"

    else:
        state["status"] = False
        state["reason"] = "Insufficient balance"
        state["route"] = "not_eligible"
    return state

def salary(state: State):
    if state["salary"] >= 25000:
        state["status"] = True
        state["route"] = "eligible"
    else:
        state["status"] = False
        state["reason"] = "Low salary"
        state["route"] = "not eligible"

    return state
    
    
def age(state:State):
    if state["age"] >= 18:
        state["status"] = True
        state["route"] = "eligible"
    else:
        state["status"] = False
        state["reason"] = "Age below 18"
        state["route"] = "not eligible"
    return state

def score(state:State):
    if state["credit_score"] > 40:
        state["status"] = True
        state["route"] = "eligible"
    else:
        state["status"] = False
        state["reason"] = "Low credit score"
        state["route"] = "not eligible"
    
    return state

def approved(state: State):

    state["final_output"] = "Loan Approved"

    return state

def not_approved(state:State):
    return state

def output(state: State):
    req_amount = state["loan_amount"]
    age = state["age"]
    score = state["credit_score"]
    if state["final_output"] == "Loan Approved":

        print(
            f"Loan Approved for amount {req_amount}, age {age}, score {score}"
        )
    
    else:
        print(
            f"Loan Rejected due to "
            f"{state['reason']}"
        )

    return state

def build_graph():
    builder = StateGraph(State)
    
    builder.add_node("INTIALIZER",intialize)
    builder.add_node("LOAN AMOUNT CHECKING",loan_amount_checking)
    builder.add_node("SALARY",salary)
    builder.add_node("AGE",age)
    builder.add_node("SCORE",score)
    builder.add_node("APPROVED",approved)
    builder.add_node("NOT APPROVED",not_approved)
    builder.add_node("OUTPUT",output)
    
    builder.add_edge(START,"INTIALIZER")
    builder.add_edge("INTIALIZER","LOAN AMOUNT CHECKING")
    
    builder.add_conditional_edges(
        "LOAN AMOUNT CHECKING",
        route_decide,
        {
            "eligible" : "SALARY",
            "not eligible": "NOT APPROVED"     
        }
    )
    
    builder.add_conditional_edges(
        "SALARY",
        route_decide,
        {
            "eligible" : "AGE",
            "not eligible": "NOT APPROVED"
        }
    )
    builder.add_conditional_edges(
        "AGE",
        route_decide,
        {
            "eligible":"SCORE",
            "not eligible": "NOT APPROVED" 
        }
    )
    
    builder.add_conditional_edges(
        "SCORE",
        route_decide,
        {
            "eligible" : "APPROVED",
            "not eligible": "NOT APPROVED" 
        }
    )
    
    builder.add_edge("APPROVED","OUTPUT")
    builder.add_edge("NOT APPROVED","OUTPUT")
    builder.add_edge("OUTPUT",END)
    
    graph = builder.compile()

    save_graph_as_png(graph,__file__)

    return graph

graph = build_graph()  

def main():

    input_data = {
        "age": 25,
        "salary": 50000,
        "credit_score": 75,
        "loan_amount": 10000
    }
    response = graph.invoke(input_data)
    print("\nFinal State:\n")
    print(response)


    input_data = {
        "age": 11,
        "salary": 50000,
        "credit_score": 75,
        "loan_amount": 10000
    }
    response = graph.invoke(input_data)
    print("\nFinal State:\n")
    print(response)
    print()

    input_data = {
        "age": 25,
        "salary": 1000,
        "credit_score": 75,
        "loan_amount": 10000
    }
    response = graph.invoke(input_data)
    print("\nFinal State:\n")
    print(response)
    print()
    
    input_data = {
        "age": 25,
        "salary": 50000,
        "credit_score": 10,
        "loan_amount": 10000
    }
    response = graph.invoke(input_data)
    print("\nFinal State:\n")
    print(response)
    print()
    
    nput_data = {
        "age": 25,
        "salary": 400,
        "credit_score": 75,
        "loan_amount": 60000
    }
    response = graph.invoke(input_data)
    print("\nFinal State:\n")
    print(response)
    print()
if __name__ == "__main__":

    main()
    
