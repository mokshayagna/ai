from dotenv import load_dotenv
load_dotenv()

from functools import partial

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from e2b_code_interpreter import Sandbox
sandbox = None

@tool
def create_sandbox():
    """Create a new E2B sandbox session."""

    global sandbox
    sandbox = Sandbox.create()

    return "Sandbox created successfully."

@tool
def write_code(code: str):
    """Write Python code to prime.py."""

    global sandbox

    if sandbox is None:
        return "Sandbox not created."

    sandbox.files.write(
        "/home/user/prime.py",
        code.encode()
    )

    return "Code written successfully."

@tool
def run_code():
    """Run prime.py and return output."""

    global sandbox

    if sandbox is None:
        return "Sandbox not created."

    result = sandbox.commands.run("python /home/user/prime.py")

    return result.stdout

tools = [
    create_sandbox,
    write_code,
    run_code
]

def ask_llm(state: MessagesState, llm):
    sys_msg = smsg = """
You are a Python coding agent.

Follow these steps:
1. Call create_sandbox.
2. Generate Python code.
3. Call write_code with the generated code.
4. Call run_code.
5. Return the output.
"""

    response = llm.invoke([sys_msg] + state["messages"])

    return {"messages": [response]}

def build_graph():
    model = ChatGoogleGenerativeAI(model= "gemini-3.5-flash")

    llm_with_tools = model.bind_tools(tools)

    builder = StateGraph(MessagesState)

    builder.add_node("ASK_LLM",partial(ask_llm, llm=llm_with_tools))

    builder.add_node("tools",ToolNode(tools))

    builder.add_edge(START, "ASK_LLM")

    builder.add_conditional_edges("ASK_LLM",tools_condition)

    builder.add_edge("tools", "ASK_LLM")

    builder.add_edge("ASK_LLM", END)

    return builder.compile()

graph = build_graph()

def main():
    query = """
Write a Python function to check whether a number is prime.
Run it for 17 and 18.
"""

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=query)
            ]
        }
    )

    for msg in result["messages"]:
        msg.pretty_print()

if __name__ == "__main__":
    main()