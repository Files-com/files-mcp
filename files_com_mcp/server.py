from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastmcp import FastMCP


_loaded_servers: set[int] = set()


def create_mcp() -> FastMCP:
    """Create a configured FastMCP server instance."""
    from files_com_mcp import patches  # noqa: F401
    from fastmcp import FastMCP

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


def create_http_app(**http_app_kwargs: Any) -> Any:
    """Create an ASGI app for HTTP deployments and wrappers."""
    mcp = create_mcp()
    return mcp.http_app(**http_app_kwargs)


def run_stdio() -> None:
    """Run the MCP server in stdio mode."""
    mcp = create_mcp()
    mcp.run(transport="stdio")


def run_server(port: int = 8000, host: str = "127.0.0.1") -> None:
    """Run the MCP server in HTTP server mode."""
    mcp = create_mcp()
    mcp.run(transport="sse", host=host, port=port)
