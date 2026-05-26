from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = "Math",host="127.0.0.1",port=3333)

# Prompts
@mcp.prompt()
def example_prompt(question: str) -> str:
    """Example prompt description"""
    return f"""
    You are a math assistant. Answer the question.
    Question: {question}
    """

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Addition of 2 numbers"""
    print(f"values of a & b are {a}, {b}")
    return int(a + b)

@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multipllication two numbers"""
    return int(a * b)

if __name__ == "__main__":
    mcp.run(transport = "streamable-http")