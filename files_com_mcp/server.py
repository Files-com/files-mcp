import importlib
from files_com_mcp import patches  # noqa: F401
from fastmcp import FastMCP
import fastmcp.settings

# Enable JSON argument parsing for tools. Claude notoriously sends JSON encoded Strings instead
#   of proper JSON list and objects, so this is a workaround to allow the MCP to use those arguments.
fastmcp.settings.settings.tool_attempt_parse_json_args = True

mcp = FastMCP("filescom")


# Dynamically load tools from the tools package
def load_tools():
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


def run_stdio():
    """Run the MCP server in stdio mode."""
    load_tools()
    mcp.run(transport="stdio")


def run_server(port: int = 8000):
    """Run the MCP server in HTTP server mode."""
    load_tools()
    mcp.run(transport="sse", host="127.0.0.1", port=port)
