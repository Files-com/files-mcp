from fastmcp import Context
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


async def list_settings_change(
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
    sort_by: Annotated[
        dict | None,
        Field(
            description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `api_key_id` or `user_id`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
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
    """List Settings Changes

    Args:
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by: If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `api_key_id` or `user_id`.
        filter: If set, return records where the specified field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
    """

    params = {}
    if cursor is not None:
        params["cursor"] = cursor
    if per_page is not None:
        params["per_page"] = per_page
    if sort_by is not None:
        params["sort_by"] = sort_by
    if filter is not None:
        params["filter"] = filter

    def call(options):
        # One page; the response tells the caller how to fetch the next.
        page = files_sdk.settings_change.list(params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
    if not retval:
        return "No settingschanges found."

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "api_key_id",
            "changes",
            "created_at",
            "user_id",
            "user_is_files_support",
            "user_is_from_parent_site",
            "username",
        ],
        fields=fields,
    )
    response = f"SettingsChange Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_Settings_Change",
        description="List Settings Changes",
        annotations={
            "title": "List Settings Change",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def list_settings_change_tool(
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
        sort_by: Annotated[
            dict | None,
            Field(
                description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `api_key_id` or `user_id`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
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
        return await list_settings_change(
            context, cursor, per_page, sort_by, filter, fields=fields
        )
