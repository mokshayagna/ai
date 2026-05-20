
from langchain_core.tools import tool

@tool
def add(a:int,b:int) -> int:
    return a+b

@tool
def sub(a:int,b:int) -> int:
    return a-b
