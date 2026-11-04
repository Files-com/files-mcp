from fastmcp import Context
from fastmcp.exceptions import ToolError
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


async def list_bundle_notification(
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
    """List Share Link Notifications

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
        page = files_sdk.bundle_notification.list(params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
    if not retval:
        return "No bundlenotifications found."

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "bundle_id",
            "id",
            "notify_on_registration",
            "notify_on_upload",
            "notify_current_user",
            "notify_user_id",
            "workspace_id",
        ],
        fields=fields,
    )
    response = f"BundleNotification Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def find_bundle_notification(
    context: Context,
    id: Annotated[
        int | None, Field(description="Bundle Notification ID.", default=None)
    ],
) -> str:
    """Show Share Link Notification

    Args:
        id: Bundle Notification ID.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        return [files_sdk.bundle_notification.find(id, params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "bundle_id",
            "id",
            "notify_on_registration",
            "notify_on_upload",
            "notify_current_user",
            "notify_user_id",
            "workspace_id",
        ],
    )
    response = f"BundleNotification Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def create_bundle_notification(
    context: Context,
    bundle_id: Annotated[
        int | None, Field(description="Bundle ID to notify on", default=None)
    ],
    notify_user_id: Annotated[
        int | None,
        Field(description="The id of the user to notify.", default=None),
    ],
    notify_on_registration: Annotated[
        bool | None,
        Field(
            description="Triggers bundle notification when a registration action occurs for it.",
            default=None,
        ),
    ],
    notify_on_upload: Annotated[
        bool | None,
        Field(
            description="Triggers bundle notification when a upload action occurs for it.",
            default=None,
        ),
    ],
) -> str:
    """Create Share Link Notification

    Args:
        bundle_id: Bundle ID to notify on
        notify_user_id: The id of the user to notify.
        notify_on_registration: Triggers bundle notification when a registration action occurs for it.
        notify_on_upload: Triggers bundle notification when a upload action occurs for it.
    """

    params = {}
    if bundle_id is None:
        raise ToolError("Missing required parameter: bundle_id")
    params["bundle_id"] = bundle_id
    if notify_user_id is not None:
        params["notify_user_id"] = notify_user_id
    if notify_on_registration is not None:
        params["notify_on_registration"] = notify_on_registration
    if notify_on_upload is not None:
        params["notify_on_upload"] = notify_on_upload

    def call(options):
        return [files_sdk.bundle_notification.create(params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "bundle_id",
            "id",
            "notify_on_registration",
            "notify_on_upload",
            "notify_current_user",
            "notify_user_id",
            "workspace_id",
        ],
    )
    response = f"BundleNotification Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def update_bundle_notification(
    context: Context,
    id: Annotated[
        int | None, Field(description="Bundle Notification ID.", default=None)
    ],
    notify_on_registration: Annotated[
        bool | None,
        Field(
            description="Triggers bundle notification when a registration action occurs for it.",
            default=None,
        ),
    ],
    notify_on_upload: Annotated[
        bool | None,
        Field(
            description="Triggers bundle notification when a upload action occurs for it.",
            default=None,
        ),
    ],
) -> str:
    """Update Share Link Notification

    Args:
        id: Bundle Notification ID.
        notify_on_registration: Triggers bundle notification when a registration action occurs for it.
        notify_on_upload: Triggers bundle notification when a upload action occurs for it.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id
    if notify_on_registration is not None:
        params["notify_on_registration"] = notify_on_registration
    if notify_on_upload is not None:
        params["notify_on_upload"] = notify_on_upload

    def call(options):
        return [
            files_sdk.bundle_notification.update(id, params, options)
        ], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "bundle_id",
            "id",
            "notify_on_registration",
            "notify_on_upload",
            "notify_current_user",
            "notify_user_id",
            "workspace_id",
        ],
    )
    response = f"BundleNotification Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def delete_bundle_notification(
    context: Context,
    id: Annotated[
        int | None, Field(description="Bundle Notification ID.", default=None)
    ],
) -> str:
    """Delete Share Link Notification

    Args:
        id: Bundle Notification ID.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        # The API returns no record for this operation.
        files_sdk.bundle_notification.delete(id, params, options)
        return [], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(retval, [])
    response = f"BundleNotification Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_Bundle_Notification",
        description="List Share Link Notifications",
        annotations={
            "title": "List Bundle Notification",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def list_bundle_notification_tool(
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
        return await list_bundle_notification(
            context, cursor, per_page, fields=fields
        )

    @mcp.tool(
        name="Find_Bundle_Notification",
        description="Show Share Link Notification",
        annotations={
            "title": "Find Bundle Notification",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def find_bundle_notification_tool(
        context: Context,
        id: Annotated[
            int | None,
            Field(description="Bundle Notification ID.", default=None),
        ],
    ) -> str:
        return await find_bundle_notification(context, id)

    @mcp.tool(
        name="Create_Bundle_Notification",
        description="Create Share Link Notification",
        annotations={
            "title": "Create Bundle Notification",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": False,
        },
    )
    async def create_bundle_notification_tool(
        context: Context,
        bundle_id: Annotated[
            int | None,
            Field(description="Bundle ID to notify on", default=None),
        ],
        notify_user_id: Annotated[
            int | None,
            Field(description="The id of the user to notify.", default=None),
        ],
        notify_on_registration: Annotated[
            bool | None,
            Field(
                description="Triggers bundle notification when a registration action occurs for it.",
                default=None,
            ),
        ],
        notify_on_upload: Annotated[
            bool | None,
            Field(
                description="Triggers bundle notification when a upload action occurs for it.",
                default=None,
            ),
        ],
    ) -> str:
        return await create_bundle_notification(
            context,
            bundle_id,
            notify_user_id,
            notify_on_registration,
            notify_on_upload,
        )

    @mcp.tool(
        name="Update_Bundle_Notification",
        description="Update Share Link Notification",
        annotations={
            "title": "Update Bundle Notification",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": True,
        },
    )
    async def update_bundle_notification_tool(
        context: Context,
        id: Annotated[
            int | None,
            Field(description="Bundle Notification ID.", default=None),
        ],
        notify_on_registration: Annotated[
            bool | None,
            Field(
                description="Triggers bundle notification when a registration action occurs for it.",
                default=None,
            ),
        ],
        notify_on_upload: Annotated[
            bool | None,
            Field(
                description="Triggers bundle notification when a upload action occurs for it.",
                default=None,
            ),
        ],
    ) -> str:
        return await update_bundle_notification(
            context, id, notify_on_registration, notify_on_upload
        )

    @mcp.tool(
        name="Delete_Bundle_Notification",
        description="Delete Share Link Notification",
        annotations={
            "title": "Delete Bundle Notification",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": True,
        },
    )
    async def delete_bundle_notification_tool(
        context: Context,
        id: Annotated[
            int | None,
            Field(description="Bundle Notification ID.", default=None),
        ],
    ) -> str:
        return await delete_bundle_notification(context, id)
