from fastmcp import Context
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.utils import (
    coerce_json,
    context_api_key,
    object_list_to_markdown_table,
)
import files_sdk
import files_sdk.error


async def list_external_event(
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
            description="Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).",
            default=None,
        ),
    ],
    sort_by: Annotated[
        dict | None,
        Field(
            description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `siem_http_destination_id`, `created_at`, `event_type`, `status` or `folder_behavior_id`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status`, `folder_behavior_id` or `siem_http_destination_id`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter_gt: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter_gteq: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter_lt: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter_lteq: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.",
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
    """List External Events

    Args:
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        sort_by: If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `siem_http_destination_id`, `created_at`, `event_type`, `status` or `folder_behavior_id`.
        filter: If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status`, `folder_behavior_id` or `siem_http_destination_id`.
        filter_gt: If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
        filter_gteq: If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
        filter_lt: If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
        filter_lteq: If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if cursor is not None:
            params["cursor"] = cursor
        if per_page is not None:
            params["per_page"] = per_page
        if sort_by is not None:
            params["sort_by"] = sort_by
        if filter is not None:
            params["filter"] = filter
        if filter_gt is not None:
            params["filter_gt"] = filter_gt
        if filter_gteq is not None:
            params["filter_gteq"] = filter_gteq
        if filter_lt is not None:
            params["filter_lt"] = filter_lt
        if filter_lteq is not None:
            params["filter_lteq"] = filter_lteq

        list_obj = files_sdk.external_event.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No externalevents found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "event_type",
                "status",
                "body",
                "created_at",
                "body_url",
                "folder_behavior_id",
                "siem_http_destination_id",
                "successful_files",
                "errored_files",
                "bytes_synced",
                "compared_files",
                "compared_folders",
                "remote_server_type",
            ],
            fields=fields,
        )
        response = f"ExternalEvent Response:\n{markdown_list}"
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
    @mcp.tool(name="List_External_Event", description="List External Events")
    async def list_external_event_tool(
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
                description="Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).",
                default=None,
            ),
        ],
        sort_by: Annotated[
            dict | None,
            Field(
                description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `siem_http_destination_id`, `created_at`, `event_type`, `status` or `folder_behavior_id`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status`, `folder_behavior_id` or `siem_http_destination_id`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter_gt: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter_gteq: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter_lt: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter_lteq: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.",
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
        return await list_external_event(
            context,
            cursor,
            per_page,
            sort_by,
            filter,
            filter_gt,
            filter_gteq,
            filter_lt,
            filter_lteq,
            fields=fields,
        )
