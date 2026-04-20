from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import context_api_key, object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_sftp_action_log(
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
            description="If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `true_path`, `remote_ip`, `session_uuid`, `success`, `status`, `action_type`, `username` or `created_at`.",
            default=None,
        ),
    ],
    filter_gt: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.",
            default=None,
        ),
    ],
    filter_gteq: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.",
            default=None,
        ),
    ],
    filter_prefix: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`, `true_path`, `action_type` or `username`.",
            default=None,
        ),
    ],
    filter_lt: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.",
            default=None,
        ),
    ],
    filter_lteq: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.",
            default=None,
        ),
    ],
    fields: Annotated[
        list[str] | None,
        Field(
            description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
            default=None,
        ),
    ],
) -> str:
    """List SFTP Action Logs

    Args:
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        filter: If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `true_path`, `remote_ip`, `session_uuid`, `success`, `status`, `action_type`, `username` or `created_at`.
        filter_gt: If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
        filter_gteq: If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
        filter_prefix: If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`, `true_path`, `action_type` or `username`.
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
        if filter_prefix is not None:
            params["filter_prefix"] = filter_prefix
        if filter_lt is not None:
            params["filter_lt"] = filter_lt
        if filter_lteq is not None:
            params["filter_lteq"] = filter_lteq

        list_obj = files_sdk.sftp_action_log.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No sftpactionlogs found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "timestamp",
                "remote_ip",
                "server_ip",
                "username",
                "ssh_client_identification",
                "session_uuid",
                "seq_id",
                "auth_method",
                "auth_ciphers",
                "action_type",
                "path",
                "true_path",
                "name",
                "sftp_response_code",
                "sftp_response_message",
                "md5",
                "size",
                "data_length",
                "bytes_transferred",
                "entries_returned",
                "success",
                "status",
                "duration_ms",
                "created_at",
            ],
            fields=fields,
        )
        response = f"SftpActionLog Response:\n{markdown_list}"
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
    @mcp.tool(name="List_Sftp_Action_Log", description="List SFTP Action Logs")
    async def list_sftp_action_log_tool(
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
                description="If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `true_path`, `remote_ip`, `session_uuid`, `success`, `status`, `action_type`, `username` or `created_at`.",
                default=None,
            ),
        ],
        filter_gt: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.",
                default=None,
            ),
        ],
        filter_gteq: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.",
                default=None,
            ),
        ],
        filter_prefix: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`, `true_path`, `action_type` or `username`.",
                default=None,
            ),
        ],
        filter_lt: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.",
                default=None,
            ),
        ],
        filter_lteq: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.",
                default=None,
            ),
        ],
        fields: Annotated[
            list[str] | None,
            Field(
                description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
                default=None,
            ),
        ],
    ) -> str:
        return await list_sftp_action_log(
            context,
            cursor,
            per_page,
            filter,
            filter_gt,
            filter_gteq,
            filter_prefix,
            filter_lt,
            filter_lteq,
            fields=fields,
        )
