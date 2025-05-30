from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_permission(
    context: Context,
    path: str | None = None,
    group_id: str | None = None,
    user_id: str | None = None,
) -> str:
    """List Permissions

    Args:
        path: Permission path.  If provided, will scope all permissions(including upward) to this path.
        group_id:
        user_id:
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if path is not None:
            params["path"] = path
        if group_id is not None:
            params["group_id"] = group_id
        if user_id is not None:
            params["user_id"] = user_id

        retval = files_sdk.permission.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
        if not retval:
            return "No permissions found."

        markdown_list = object_list_to_markdown_table(
            retval, ["path", "group_id", "user_id", "permission", "id"]
        )
        return f"Permission Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def create_permission(
    context: Context,
    path: str | None = None,
    group_id: int | None = None,
    permission: str | None = None,
    user_id: int | None = None,
) -> str:
    """Create Permission

    Args:
        path: Folder path
        group_id: Group ID. Provide `group_name` or `group_id`
        permission: Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`
        user_id: User ID.  Provide `username` or `user_id`
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path
        if group_id is not None:
            params["group_id"] = group_id
        if permission is not None:
            params["permission"] = permission
        if user_id is not None:
            params["user_id"] = user_id

        retval = files_sdk.permission.create(params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["path", "group_id", "user_id", "permission", "id"]
        )
        return f"Permission Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def delete_permission(context: Context, id: int | None = None) -> str:
    """Delete Permission

    Args:
        id: Permission ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.permission.delete(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["path", "group_id", "user_id", "permission", "id"]
        )
        return f"Permission Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_Permission")
    async def list_permission_tool(
        context: Context,
        path: str | None = None,
        group_id: str | None = None,
        user_id: str | None = None,
    ) -> str:
        return await list_permission(context, path, group_id, user_id)

    @mcp.tool(name="Create_Permission")
    async def create_permission_tool(
        context: Context,
        path: str | None = None,
        group_id: int | None = None,
        permission: str | None = None,
        user_id: int | None = None,
    ) -> str:
        return await create_permission(
            context, path, group_id, permission, user_id
        )

    @mcp.tool(name="Delete_Permission")
    async def delete_permission_tool(
        context: Context, id: int | None = None
    ) -> str:
        return await delete_permission(context, id)
