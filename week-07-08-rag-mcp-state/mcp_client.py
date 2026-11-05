"""A real MCP client; deterministic tool selection, not an LLM agent loop."""

import argparse
import asyncio
from datetime import timedelta
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from state_store import StateStore


async def run(question: str) -> None:
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("mcp_server.py"))],
    )
    async with asyncio.timeout(30):
        async with stdio_client(server) as (reader, writer):
            async with ClientSession(
                reader, writer, read_timeout_seconds=timedelta(seconds=15)
            ) as session:
                await session.initialize()
                tools = await session.list_tools()
                print("Available tools:", [tool.name for tool in tools.tools])
                result = await session.call_tool(
                    "search_documents", arguments={"question": question, "top_k": 2}
                )
                if result.isError:
                    raise RuntimeError("MCP document search failed.")
                payload = result.model_dump(mode="json")
                StateStore().append(question, payload)
                print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", default="What is FastAPI?")
    args = parser.parse_args()
    try:
        asyncio.run(run(args.question))
    except (TimeoutError, RuntimeError, ValueError, OSError):
        parser.exit(1, "MCP request failed. Check dependencies and the server.\n")
