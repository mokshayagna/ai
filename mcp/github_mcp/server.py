import sys
import os
import subprocess
import asyncio
import logging
import httpx
from mcp.server.fastmcp import FastMCP

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("mcp").setLevel(logging.WARNING)

_docker_process = None
GITHUB_URL = "http://127.0.0.1:9000/mcp"

def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def start_docker():
    global _docker_process
    _docker_process = subprocess.Popen([
        "docker", "run", "--rm", "-p", "9000:8082",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server",
        "http"
    ], env={**os.environ, "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")},
       stdout=subprocess.DEVNULL,
       stderr=subprocess.DEVNULL)
async def get_tools():
    async with httpx.AsyncClient(timeout=30.0) as client:
        init_resp = await client.post(GITHUB_URL, headers=get_headers(), json={
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "proxy", "version": "1.0"}
            }
        })
        session_id = init_resp.headers.get("mcp-session-id")
        headers = {**get_headers(), "mcp-session-id": session_id}

        resp = await client.post(GITHUB_URL, headers=headers, json={
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
        })
        
        # parse SSE format
        import json
        for line in resp.text.splitlines():
            if line.startswith("data:"):
                data = json.loads(line[5:].strip())
                return data.get("result", {}).get("tools", [])
        return []


async def github_call(tool_name: str, arguments: dict) -> str:
    import json
    async with httpx.AsyncClient(timeout=30.0) as client:
        init_resp = await client.post(GITHUB_URL, headers=get_headers(), json={
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "proxy", "version": "1.0"}
            }
        })
        session_id = init_resp.headers.get("mcp-session-id")
        headers = {**get_headers(), "mcp-session-id": session_id}

        resp = await client.post(GITHUB_URL, headers=headers, json={
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments}
        })

        # parse SSE format
        for line in resp.text.splitlines():
            if line.startswith("data:"):
                data = json.loads(line[5:].strip())
                if "result" in data:
                    content = data["result"].get("content", [])
                    if content:
                        return content[0].get("text", "No result")
                if "error" in data:
                    return f"Error: {data['error']}"
        return "No result"
async def setup():
    start_docker()
    print("Waiting for docker to start...", file=sys.stderr)
    await asyncio.sleep(4)
    print("Connected to GitHub MCP server.", file=sys.stderr)
    return await get_tools()

if __name__ == "__main__":
    print("Starting GitHub MCP proxy server...", file=sys.stderr)

    tools = asyncio.run(setup())

    mcp = FastMCP(name="GitHub MCP Proxy", host="127.0.0.1", port=8000)

    for tool in tools:
        tool_name = tool["name"]
        tool_desc = tool.get("description", "")

        def make_tool_fn(name):
            async def tool_fn(kwargs: dict) -> str:
                try:
                    return await github_call(name, kwargs)
                except Exception as e:
                    return f"Error: {type(e).__name__}: {e}"
            tool_fn.__name__ = name
            tool_fn.__doc__ = tool_desc
            return tool_fn

        mcp.tool()(make_tool_fn(tool_name))

    try:
        mcp.run(transport='streamable-http')
    finally:
        if _docker_process:
            _docker_process.terminate()
            print("Docker container stopped.", file=sys.stderr)