from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import context_api_key, object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_permission(
    context: Context,
    path: Annotated[
        str | None,
        Field(
            description="Permission path.  If provided, will scope all permissions(including upward) to this path.",
            default=None,
        ),
    ],
    group_id: Annotated[str | None, Field(description="", default=None)],
    user_id: Annotated[str | None, Field(description="", default=None)],
    fields: Annotated[
        list[str] | None,
        Field(
            description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
            default=None,
        ),
    ],
) -> str:
    """List Permissions

    Args:
        path: Permission path.  If provided, will scope all permissions(including upward) to this path.
        group_id:
        user_id:
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is not None:
            params["path"] = path
        if group_id is not None:
            params["group_id"] = group_id
        if user_id is not None:
            params["user_id"] = user_id

        list_obj = files_sdk.permission.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No permissions found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "user_id",
                "username",
                "group_id",
                "group_name",
                "group_ids",
                "group_names",
                "partner_id",
                "partner_name",
                "permission",
                "recursive",
                "site_id",
            ],
            fields=fields,
        )
        response = f"Permission Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def create_permission(
    context: Context,
    path: Annotated[
        str | None, Field(description="Folder path", default=None)
    ],
    group_id: Annotated[
        int | None,
        Field(
            description="Group ID. Provide `group_name` or `group_id`",
            default=None,
        ),
    ],
    permission: Annotated[
        str | None,
        Field(
            description="Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`",
            default=None,
        ),
    ],
    user_id: Annotated[
        int | None,
        Field(
            description="User ID.  Provide `username` or `user_id`",
            default=None,
        ),
    ],
) -> str:
    """Create Permission

    Args:
        path: Folder path
        group_id: Group ID. Provide `group_name` or `group_id`
        permission: Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`
        user_id: User ID.  Provide `username` or `user_id`
    """

    try:
        options = {"api_key": context_api_key(context)}
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
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "user_id",
                "username",
                "group_id",
                "group_name",
                "group_ids",
                "group_names",
                "partner_id",
                "partner_name",
                "permission",
                "recursive",
                "site_id",
            ],
        )
        response = f"Permission Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def delete_permission(
    context: Context,
    id: Annotated[
        int | None, Field(description="Permission ID.", default=None)
    ],
) -> str:
    """Delete Permission

    Args:
        id: Permission ID.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.permission.delete(id, params, options)
        retval = [retval]
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "user_id",
                "username",
                "group_id",
                "group_name",
                "group_ids",
                "group_names",
                "partner_id",
                "partner_name",
                "permission",
                "recursive",
                "site_id",
            ],
        )
        response = f"Permission Response:\n{markdown_list}"
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
    @mcp.tool(name="List_Permission", description="List Permissions")
    async def list_permission_tool(
        context: Context,
        path: Annotated[
            str | None,
            Field(
                description="Permission path.  If provided, will scope all permissions(including upward) to this path.",
                default=None,
            ),
        ],
        group_id: Annotated[str | None, Field(description="", default=None)],
        user_id: Annotated[str | None, Field(description="", default=None)],
        fields: Annotated[
            list[str] | None,
            Field(
                description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
                default=None,
            ),
        ],
    ) -> str:
        return await list_permission(
            context, path, group_id, user_id, fields=fields
        )

    @mcp.tool(name="Create_Permission", description="Create Permission")
    async def create_permission_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Folder path", default=None)
        ],
        group_id: Annotated[
            int | None,
            Field(
                description="Group ID. Provide `group_name` or `group_id`",
                default=None,
            ),
        ],
        permission: Annotated[
            str | None,
            Field(
                description="Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`",
                default=None,
            ),
        ],
        user_id: Annotated[
            int | None,
            Field(
                description="User ID.  Provide `username` or `user_id`",
                default=None,
            ),
        ],
    ) -> str:
        return await create_permission(
            context, path, group_id, permission, user_id
        )

    @mcp.tool(name="Delete_Permission", description="Delete Permission")
    async def delete_permission_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Permission ID.", default=None)
        ],
    ) -> str:
        return await delete_permission(context, id)
