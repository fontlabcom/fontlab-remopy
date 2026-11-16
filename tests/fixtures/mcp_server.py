# this_file: tests/fixtures/mcp_server.py
# SPDX-License-Identifier: Apache-2.0
"""Real SDK server fixture; never touches FontLab or invokes an LLM provider."""

import os
from pathlib import Path

try:  # MCP SDK v2 renamed FastMCP to MCPServer
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FontLab fixture")


@mcp.tool()
def list_fonts() -> list[dict]:
    """List fixture fonts, recording actual execution for the end-to-end test."""
    Path(os.environ["AIDUS_MCP_TEST_LOG"]).write_text("list_fonts called", encoding="utf-8")
    return [{"id": "fixture-font", "family": "Fixture"}]


@mcp.tool()
def run_python(code: str) -> str:
    """Fixture mutation, used only to check role isolation."""
    return code


if __name__ == "__main__":
    mcp.run(transport="stdio")
