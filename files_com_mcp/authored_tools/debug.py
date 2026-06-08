async def hello_world() -> str:
    """Files.com MCP Debugging Hello World function."""
    return "Hello World"


def register_tools(mcp):
    @mcp.tool(
        name="Hello_World",
        description="Files.com MCP Debugging Hello World function.",
        annotations={
            "title": "Hello World",
            "readOnlyHint": True,
            "openWorldHint": False,
        },
    )
    async def hello_world_tool() -> str:
        return await hello_world()
