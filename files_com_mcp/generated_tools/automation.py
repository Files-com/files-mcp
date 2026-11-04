from fastmcp import Context
from fastmcp.exceptions import ToolError
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


async def list_automation(
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
    """List Automations

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
        page = files_sdk.automation.list(params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
    if not retval:
        return "No automations found."

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "id",
            "workspace_id",
            "always_serialize_jobs",
            "always_overwrite_size_matching_files",
            "automation",
            "converted_automation_id",
            "deleted",
            "description",
            "definition",
            "destination_replace_from",
            "destination_replace_to",
            "destinations",
            "disabled",
            "exclude_pattern",
            "import_urls",
            "inbound_email_address",
            "flatten_destination_structure",
            "group_ids",
            "ignore_locked_folders",
            "interval",
            "last_modified_at",
            "legacy_folder_matching",
            "name",
            "original_automation_id",
            "overwrite_files",
            "path",
            "path_time_zone",
            "version",
            "recurring_day",
            "recurring_days",
            "schedule_id",
            "retry_on_failure_interval_in_minutes",
            "retry_on_failure_number_of_attempts",
            "schedule",
            "human_readable_schedule",
            "schedule_days_of_week",
            "schedule_times_of_day",
            "schedule_time_zone",
            "source",
            "sync_ids",
            "trigger_actions",
            "trigger",
            "user_id",
            "user_ids",
            "value",
            "webhook_url",
            "holiday_region",
        ],
        fields=fields,
    )
    response = f"Automation Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def find_automation(
    context: Context,
    id: Annotated[
        int | None, Field(description="Automation ID.", default=None)
    ],
) -> str:
    """Show Automation

    Args:
        id: Automation ID.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        return [files_sdk.automation.find(id, params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "id",
            "workspace_id",
            "always_serialize_jobs",
            "always_overwrite_size_matching_files",
            "automation",
            "converted_automation_id",
            "deleted",
            "description",
            "definition",
            "destination_replace_from",
            "destination_replace_to",
            "destinations",
            "disabled",
            "exclude_pattern",
            "import_urls",
            "inbound_email_address",
            "flatten_destination_structure",
            "group_ids",
            "ignore_locked_folders",
            "interval",
            "last_modified_at",
            "legacy_folder_matching",
            "name",
            "original_automation_id",
            "overwrite_files",
            "path",
            "path_time_zone",
            "version",
            "recurring_day",
            "recurring_days",
            "schedule_id",
            "retry_on_failure_interval_in_minutes",
            "retry_on_failure_number_of_attempts",
            "schedule",
            "human_readable_schedule",
            "schedule_days_of_week",
            "schedule_times_of_day",
            "schedule_time_zone",
            "source",
            "sync_ids",
            "trigger_actions",
            "trigger",
            "user_id",
            "user_ids",
            "value",
            "webhook_url",
            "holiday_region",
        ],
    )
    response = f"Automation Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_Automation",
        description="List Automations",
        annotations={
            "title": "List Automation",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def list_automation_tool(
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
        return await list_automation(context, cursor, per_page, fields=fields)

    @mcp.tool(
        name="Find_Automation",
        description="Show Automation",
        annotations={
            "title": "Find Automation",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def find_automation_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Automation ID.", default=None)
        ],
    ) -> str:
        return await find_automation(context, id)
