from fastmcp import Context
from fastmcp.exceptions import ToolError
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


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
    cursor: Annotated[
        str | None,
        Field(
            description="Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.",
            default=None,
        ),
    ],
    per_page: Annotated[
        int | None,
        Field(
            description="Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).",
            default=None,
        ),
    ],
    fields: Annotated[
        list[str] | None,
        Field(
            description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
) -> str:
    """List Permissions

    Args:
        path: Permission path.  If provided, will scope all permissions(including upward) to this path.
        group_id:
        user_id:
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """

    params = {}
    if path is not None:
        params["path"] = path
    if group_id is not None:
        params["group_id"] = group_id
    if user_id is not None:
        params["user_id"] = user_id
    if cursor is not None:
        params["cursor"] = cursor
    if per_page is not None:
        params["per_page"] = per_page

    def call(options):
        # One page; the response tells the caller how to fetch the next.
        page = files_sdk.permission.list(params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
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

    params = {}
    if path is None:
        raise ToolError("Missing required parameter: path")
    params["path"] = path
    if group_id is not None:
        params["group_id"] = group_id
    if permission is not None:
        params["permission"] = permission
    if user_id is not None:
        params["user_id"] = user_id

    def call(options):
        return [files_sdk.permission.create(params, options)], None

    retval, next_cursor = await call_files_api(context, call)

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

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        # The API returns no record for this operation.
        files_sdk.permission.delete(id, params, options)
        return [], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(retval, [])
    response = f"Permission Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_Permission",
        description="List Permissions",
        annotations={
            "title": "List Permission",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
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
        cursor: Annotated[
            str | None,
            Field(
                description="Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.",
                default=None,
            ),
        ],
        per_page: Annotated[
            int | None,
            Field(
                description="Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).",
                default=None,
            ),
        ],
        fields: Annotated[
            list[str] | None,
            Field(
                description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
    ) -> str:
        return await list_permission(
            context, path, group_id, user_id, cursor, per_page, fields=fields
        )

    @mcp.tool(
        name="Create_Permission",
        description="Create Permission",
        annotations={
            "title": "Create Permission",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": False,
        },
    )
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

    @mcp.tool(
        name="Delete_Permission",
        description="Delete Permission",
        annotations={
            "title": "Delete Permission",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": True,
        },
    )
    async def delete_permission_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Permission ID.", default=None)
        ],
    ) -> str:
        return await delete_permission(context, id)
