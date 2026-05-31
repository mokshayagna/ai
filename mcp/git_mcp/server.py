from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHub MCP")

TOOLS = [
    {
        "name":"list_repositories",
        "description":"List github repositories"
    },

    {
        "name":"create_issue",
        "description":"Create issue"
    },

    {
        "name":"create_pull_request",
        "description":"Create pull request"
    },

    {
        "name":"read_file",
        "description":"Read repository file"
    }
]

for tool in TOOLS:

    mcp.add_tool(
        name=tool["name"],
        description=tool["description"]
    )

if __name__=="__main__":

    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=3333
    )