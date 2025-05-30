from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_remote_server(context: Context) -> str:
    """List Remote Servers"""

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}

        retval = files_sdk.remote_server.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
        if not retval:
            return "No remoteservers found."

        markdown_list = object_list_to_markdown_table(
            retval, ["id", "name", "server_type"]
        )
        return f"RemoteServer Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def find_remote_server(context: Context, id: int | None = None) -> str:
    """Show Remote Server

    Args:
        id: Remote Server ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.remote_server.find(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["id", "name", "server_type"]
        )
        return f"RemoteServer Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_Remote_Server")
    async def list_remote_server_tool(context: Context) -> str:
        return await list_remote_server(context)

    @mcp.tool(name="Find_Remote_Server")
    async def find_remote_server_tool(
        context: Context, id: int | None = None
    ) -> str:
        return await find_remote_server(context, id)
