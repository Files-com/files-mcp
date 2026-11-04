from fastmcp import Context
from fastmcp.exceptions import ToolError
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


async def list_group(
    context: Context,
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
    """List Groups

    Args:
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """

    params = {}
    if cursor is not None:
        params["cursor"] = cursor
    if per_page is not None:
        params["per_page"] = per_page

    def call(options):
        # One page; the response tells the caller how to fetch the next.
        page = files_sdk.group.list(params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
    if not retval:
        return "No groups found."

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "id",
            "name",
            "allowed_ips",
            "admin_ids",
            "notes",
            "user_ids",
            "usernames",
            "ai_assistant_personality_id",
            "ftp_permission",
            "sftp_permission",
            "dav_permission",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
            "site_id",
            "workspace_id",
        ],
        fields=fields,
    )
    response = f"Group Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def find_group(
    context: Context,
    id: Annotated[int | None, Field(description="Group ID.", default=None)],
) -> str:
    """Show Group

    Args:
        id: Group ID.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        return [files_sdk.group.find(id, params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "id",
            "name",
            "allowed_ips",
            "admin_ids",
            "notes",
            "user_ids",
            "usernames",
            "ai_assistant_personality_id",
            "ftp_permission",
            "sftp_permission",
            "dav_permission",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
            "site_id",
            "workspace_id",
        ],
    )
    response = f"Group Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def create_group(
    context: Context,
    name: Annotated[
        str | None, Field(description="Group name.", default=None)
    ],
    notes: Annotated[
        str | None, Field(description="Group notes.", default=None)
    ],
    user_ids: Annotated[
        str | None,
        Field(
            description="A list of user ids. If sent as a string, should be comma-delimited.",
            default=None,
        ),
    ],
    admin_ids: Annotated[
        str | None,
        Field(
            description="A list of group admin user ids. If sent as a string, should be comma-delimited.",
            default=None,
        ),
    ],
) -> str:
    """Create Group

    Args:
        name: Group name.
        notes: Group notes.
        user_ids: A list of user ids. If sent as a string, should be comma-delimited.
        admin_ids: A list of group admin user ids. If sent as a string, should be comma-delimited.
    """

    params = {}
    if name is None:
        raise ToolError("Missing required parameter: name")
    params["name"] = name
    if notes is not None:
        params["notes"] = notes
    if user_ids is not None:
        params["user_ids"] = user_ids
    if admin_ids is not None:
        params["admin_ids"] = admin_ids

    def call(options):
        return [files_sdk.group.create(params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "id",
            "name",
            "allowed_ips",
            "admin_ids",
            "notes",
            "user_ids",
            "usernames",
            "ai_assistant_personality_id",
            "ftp_permission",
            "sftp_permission",
            "dav_permission",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
            "site_id",
            "workspace_id",
        ],
    )
    response = f"Group Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def update_group(
    context: Context,
    id: Annotated[int | None, Field(description="Group ID.", default=None)],
    notes: Annotated[
        str | None, Field(description="Group notes.", default=None)
    ],
    user_ids: Annotated[
        str | None,
        Field(
            description="A list of user ids. If sent as a string, should be comma-delimited.",
            default=None,
        ),
    ],
    admin_ids: Annotated[
        str | None,
        Field(
            description="A list of group admin user ids. If sent as a string, should be comma-delimited.",
            default=None,
        ),
    ],
    name: Annotated[
        str | None, Field(description="Group name.", default=None)
    ],
) -> str:
    """Update Group

    Args:
        id: Group ID.
        notes: Group notes.
        user_ids: A list of user ids. If sent as a string, should be comma-delimited.
        admin_ids: A list of group admin user ids. If sent as a string, should be comma-delimited.
        name: Group name.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id
    if notes is not None:
        params["notes"] = notes
    if user_ids is not None:
        params["user_ids"] = user_ids
    if admin_ids is not None:
        params["admin_ids"] = admin_ids
    if name is not None:
        params["name"] = name

    def call(options):
        return [files_sdk.group.update(id, params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "id",
            "name",
            "allowed_ips",
            "admin_ids",
            "notes",
            "user_ids",
            "usernames",
            "ai_assistant_personality_id",
            "ftp_permission",
            "sftp_permission",
            "dav_permission",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
            "site_id",
            "workspace_id",
        ],
    )
    response = f"Group Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def delete_group(
    context: Context,
    id: Annotated[int | None, Field(description="Group ID.", default=None)],
) -> str:
    """Delete Group

    Args:
        id: Group ID.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        # The API returns no record for this operation.
        files_sdk.group.delete(id, params, options)
        return [], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(retval, [])
    response = f"Group Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_Group",
        description="List Groups",
        annotations={
            "title": "List Group",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def list_group_tool(
        context: Context,
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
        return await list_group(context, cursor, per_page, fields=fields)

    @mcp.tool(
        name="Find_Group",
        description="Show Group",
        annotations={
            "title": "Find Group",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def find_group_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Group ID.", default=None)
        ],
    ) -> str:
        return await find_group(context, id)

    @mcp.tool(
        name="Create_Group",
        description="Create Group",
        annotations={
            "title": "Create Group",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": False,
        },
    )
    async def create_group_tool(
        context: Context,
        name: Annotated[
            str | None, Field(description="Group name.", default=None)
        ],
        notes: Annotated[
            str | None, Field(description="Group notes.", default=None)
        ],
        user_ids: Annotated[
            str | None,
            Field(
                description="A list of user ids. If sent as a string, should be comma-delimited.",
                default=None,
            ),
        ],
        admin_ids: Annotated[
            str | None,
            Field(
                description="A list of group admin user ids. If sent as a string, should be comma-delimited.",
                default=None,
            ),
        ],
    ) -> str:
        return await create_group(context, name, notes, user_ids, admin_ids)

    @mcp.tool(
        name="Update_Group",
        description="Update Group",
        annotations={
            "title": "Update Group",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": True,
        },
    )
    async def update_group_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Group ID.", default=None)
        ],
        notes: Annotated[
            str | None, Field(description="Group notes.", default=None)
        ],
        user_ids: Annotated[
            str | None,
            Field(
                description="A list of user ids. If sent as a string, should be comma-delimited.",
                default=None,
            ),
        ],
        admin_ids: Annotated[
            str | None,
            Field(
                description="A list of group admin user ids. If sent as a string, should be comma-delimited.",
                default=None,
            ),
        ],
        name: Annotated[
            str | None, Field(description="Group name.", default=None)
        ],
    ) -> str:
        return await update_group(
            context, id, notes, user_ids, admin_ids, name
        )

    @mcp.tool(
        name="Delete_Group",
        description="Delete Group",
        annotations={
            "title": "Delete Group",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": True,
        },
    )
    async def delete_group_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Group ID.", default=None)
        ],
    ) -> str:
        return await delete_group(context, id)
