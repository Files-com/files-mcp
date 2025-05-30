import requests


async def check_platform_status() -> str:
    """Check Files.com platform status at status.files.com."""
    url = "https://status.files.com/api/v2/status.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return (
                response.json()
                .get("status", {})
                .get("description", "Error processing the status page")
            )
        else:
            return "Error connecting to status page"
    except requests.exceptions.RequestException:
        return "Error connecting to status page"


def register_tools(mcp):
    @mcp.tool(name="Check_Platform_Status")
    async def check_platform_status_tool() -> str:
        return await check_platform_status()
