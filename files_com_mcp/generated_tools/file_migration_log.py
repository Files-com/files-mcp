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


async def list_file_migration_log(
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
    filter: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is equal to the supplied value. Valid fields are `file_migration_id`, `operation`, `status`, `type` or `created_at`.",
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
    """List File Migration Logs

    Args:
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        filter: If set, return records where the specified field is equal to the supplied value. Valid fields are `file_migration_id`, `operation`, `status`, `type` or `created_at`.
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

        list_obj = files_sdk.file_migration_log.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No filemigrationlogs found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "timestamp",
                "file_migration_id",
                "dest_path",
                "error_type",
                "message",
                "operation",
                "path",
                "status",
                "created_at",
            ],
            fields=fields,
        )
        response = f"FileMigrationLog Response:\n{markdown_list}"
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
    @mcp.tool(
        name="List_File_Migration_Log", description="List File Migration Logs"
    )
    async def list_file_migration_log_tool(
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
        filter: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is equal to the supplied value. Valid fields are `file_migration_id`, `operation`, `status`, `type` or `created_at`.",
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
        return await list_file_migration_log(
            context,
            cursor,
            per_page,
            filter,
            filter_gt,
            filter_gteq,
            filter_lt,
            filter_lteq,
            fields=fields,
        )
