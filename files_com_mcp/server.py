from __future__ import annotations

import importlib
import os
from typing import TYPE_CHECKING

import files_sdk

if TYPE_CHECKING:
    from fastmcp import FastMCP


_loaded_servers: set[int] = set()


def _apply_api_key_setting() -> None:
    api_key = os.getenv("FILES_COM_API_KEY", "").strip()
    if api_key:
        files_sdk.set_api_key(api_key)


def create_mcp() -> FastMCP:
    """Create a configured FastMCP server instance."""
    from files_com_mcp import patches  # noqa: F401
    from fastmcp import FastMCP

    _apply_api_key_setting()
    mcp = FastMCP("filescom")
    load_tools(mcp)
    return mcp


def load_tools(mcp: FastMCP) -> None:
    """Dynamically load and register tool modules on a server."""
    if id(mcp) in _loaded_servers:
        return

    # Authored tools
    from files_com_mcp.authored_tools import tool_list as authored_tool_modules

    for module_name in authored_tool_modules:
        module = importlib.import_module(
            f"files_com_mcp.authored_tools.{module_name}"
        )
        if hasattr(module, "register_tools"):
            module.register_tools(mcp)

    # Generated tools
    from files_com_mcp.generated_tools import (
        tool_list as generated_tool_modules,
    )

    for module_name in generated_tool_modules:
        module = importlib.import_module(
            f"files_com_mcp.generated_tools.{module_name}"
        )
        if hasattr(module, "register_tools"):
            module.register_tools(mcp)

    _loaded_servers.add(id(mcp))


def run_stdio() -> None:
    """Run the MCP server in stdio mode."""
    mcp = create_mcp()
    mcp.run(transport="stdio")
