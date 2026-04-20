from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import context_api_key, object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_remote_server(
    context: Context,
    fields: Annotated[
        list[str] | None,
        Field(
            description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
            default=None,
        ),
    ],
) -> str:
    """List Remote Servers"""

    try:
        options = {"api_key": context_api_key(context)}
        params = {}

        list_obj = files_sdk.remote_server.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No remoteservers found."

        markdown_list = object_list_to_markdown_table(
            retval, ["id", "name", "server_type"], fields=fields
        )
        response = f"RemoteServer Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def find_remote_server(
    context: Context,
    id: Annotated[
        int | None, Field(description="Remote Server ID.", default=None)
    ],
) -> str:
    """Show Remote Server

    Args:
        id: Remote Server ID.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.remote_server.find(id, params, options)
        retval = [retval]
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval, ["id", "name", "server_type"]
        )
        response = f"RemoteServer Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_Remote_Server", description="List Remote Servers")
    async def list_remote_server_tool(
        context: Context,
        fields: Annotated[
            list[str] | None,
            Field(
                description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
                default=None,
            ),
        ],
    ) -> str:
        return await list_remote_server(context, fields=fields)

    @mcp.tool(name="Find_Remote_Server", description="Show Remote Server")
    async def find_remote_server_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Remote Server ID.", default=None)
        ],
    ) -> str:
        return await find_remote_server(context, id)
