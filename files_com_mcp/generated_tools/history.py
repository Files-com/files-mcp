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


async def list_for_file_history(
    context: Context,
    start_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter earlier entries.",
            default=None,
        ),
    ],
    end_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter later entries.",
            default=None,
        ),
    ],
    display: Annotated[
        str | None,
        Field(
            description="Display format. Leave blank or set to `full` or `parent`.",
            default=None,
        ),
    ],
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
            description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
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
    """List history for specific file.

    Args:
        start_at: Leave blank or set to a date/time to filter earlier entries.
        end_at: Leave blank or set to a date/time to filter later entries.
        display: Display format. Leave blank or set to `full` or `parent`.
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        sort_by: If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        path: Path to operate on.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if start_at is not None:
            params["start_at"] = start_at
        if end_at is not None:
            params["end_at"] = end_at
        if display is not None:
            params["display"] = display
        if cursor is not None:
            params["cursor"] = cursor
        if per_page is not None:
            params["per_page"] = per_page
        if sort_by is not None:
            params["sort_by"] = sort_by
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        list_obj = files_sdk.history.list_for_file(path, params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No histories found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "when",
                "destination",
                "display",
                "ip",
                "source",
                "targets",
                "user_id",
                "username",
                "action",
                "failure_type",
                "interface",
            ],
            fields=fields,
        )
        response = f"History Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_for_folder_history(
    context: Context,
    start_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter earlier entries.",
            default=None,
        ),
    ],
    end_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter later entries.",
            default=None,
        ),
    ],
    display: Annotated[
        str | None,
        Field(
            description="Display format. Leave blank or set to `full` or `parent`.",
            default=None,
        ),
    ],
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
            description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
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
    """List history for specific folder.

    Args:
        start_at: Leave blank or set to a date/time to filter earlier entries.
        end_at: Leave blank or set to a date/time to filter later entries.
        display: Display format. Leave blank or set to `full` or `parent`.
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        sort_by: If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        path: Path to operate on.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if start_at is not None:
            params["start_at"] = start_at
        if end_at is not None:
            params["end_at"] = end_at
        if display is not None:
            params["display"] = display
        if cursor is not None:
            params["cursor"] = cursor
        if per_page is not None:
            params["per_page"] = per_page
        if sort_by is not None:
            params["sort_by"] = sort_by
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        list_obj = files_sdk.history.list_for_folder(path, params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No histories found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "when",
                "destination",
                "display",
                "ip",
                "source",
                "targets",
                "user_id",
                "username",
                "action",
                "failure_type",
                "interface",
            ],
            fields=fields,
        )
        response = f"History Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_for_user_history(
    context: Context,
    start_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter earlier entries.",
            default=None,
        ),
    ],
    end_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter later entries.",
            default=None,
        ),
    ],
    display: Annotated[
        str | None,
        Field(
            description="Display format. Leave blank or set to `full` or `parent`.",
            default=None,
        ),
    ],
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
            description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    user_id: Annotated[
        int | None, Field(description="User ID.", default=None)
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
    """List history for specific user.

    Args:
        start_at: Leave blank or set to a date/time to filter earlier entries.
        end_at: Leave blank or set to a date/time to filter later entries.
        display: Display format. Leave blank or set to `full` or `parent`.
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        sort_by: If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        user_id: User ID.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if start_at is not None:
            params["start_at"] = start_at
        if end_at is not None:
            params["end_at"] = end_at
        if display is not None:
            params["display"] = display
        if cursor is not None:
            params["cursor"] = cursor
        if per_page is not None:
            params["per_page"] = per_page
        if sort_by is not None:
            params["sort_by"] = sort_by
        if user_id is None:
            return "Missing required parameter: user_id"
        params["user_id"] = user_id

        list_obj = files_sdk.history.list_for_user(user_id, params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No histories found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "when",
                "destination",
                "display",
                "ip",
                "source",
                "targets",
                "user_id",
                "username",
                "action",
                "failure_type",
                "interface",
            ],
            fields=fields,
        )
        response = f"History Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_logins_history(
    context: Context,
    start_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter earlier entries.",
            default=None,
        ),
    ],
    end_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter later entries.",
            default=None,
        ),
    ],
    display: Annotated[
        str | None,
        Field(
            description="Display format. Leave blank or set to `full` or `parent`.",
            default=None,
        ),
    ],
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
            description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
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
    """List site login history.

    Args:
        start_at: Leave blank or set to a date/time to filter earlier entries.
        end_at: Leave blank or set to a date/time to filter later entries.
        display: Display format. Leave blank or set to `full` or `parent`.
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        sort_by: If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if start_at is not None:
            params["start_at"] = start_at
        if end_at is not None:
            params["end_at"] = end_at
        if display is not None:
            params["display"] = display
        if cursor is not None:
            params["cursor"] = cursor
        if per_page is not None:
            params["per_page"] = per_page
        if sort_by is not None:
            params["sort_by"] = sort_by

        list_obj = files_sdk.history.list_logins(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No histories found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "when",
                "destination",
                "display",
                "ip",
                "source",
                "targets",
                "user_id",
                "username",
                "action",
                "failure_type",
                "interface",
            ],
            fields=fields,
        )
        response = f"History Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_history(
    context: Context,
    start_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter earlier entries.",
            default=None,
        ),
    ],
    end_at: Annotated[
        str | None,
        Field(
            description="Leave blank or set to a date/time to filter later entries.",
            default=None,
        ),
    ],
    display: Annotated[
        str | None,
        Field(
            description="Display format. Leave blank or set to `full` or `parent`.",
            default=None,
        ),
    ],
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
            description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is equal to the supplied value. Valid fields are `user_id`, `folder` or `path`.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
    filter_prefix: Annotated[
        dict | None,
        Field(
            description="If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.",
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
    """List site full action history.

    Args:
        start_at: Leave blank or set to a date/time to filter earlier entries.
        end_at: Leave blank or set to a date/time to filter later entries.
        display: Display format. Leave blank or set to `full` or `parent`.
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
        sort_by: If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        filter: If set, return records where the specified field is equal to the supplied value. Valid fields are `user_id`, `folder` or `path`.
        filter_prefix: If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if start_at is not None:
            params["start_at"] = start_at
        if end_at is not None:
            params["end_at"] = end_at
        if display is not None:
            params["display"] = display
        if cursor is not None:
            params["cursor"] = cursor
        if per_page is not None:
            params["per_page"] = per_page
        if sort_by is not None:
            params["sort_by"] = sort_by
        if filter is not None:
            params["filter"] = filter
        if filter_prefix is not None:
            params["filter_prefix"] = filter_prefix

        list_obj = files_sdk.history.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No histories found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "path",
                "when",
                "destination",
                "display",
                "ip",
                "source",
                "targets",
                "user_id",
                "username",
                "action",
                "failure_type",
                "interface",
            ],
            fields=fields,
        )
        response = f"History Response:\n{markdown_list}"
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
        name="List_For_File_History",
        description="List history for specific file.",
    )
    async def list_for_file_history_tool(
        context: Context,
        start_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter earlier entries.",
                default=None,
            ),
        ],
        end_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter later entries.",
                default=None,
            ),
        ],
        display: Annotated[
            str | None,
            Field(
                description="Display format. Leave blank or set to `full` or `parent`.",
                default=None,
            ),
        ],
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
                description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
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
        return await list_for_file_history(
            context,
            start_at,
            end_at,
            display,
            cursor,
            per_page,
            sort_by,
            path,
            fields=fields,
        )

    @mcp.tool(
        name="List_For_Folder_History",
        description="List history for specific folder.",
    )
    async def list_for_folder_history_tool(
        context: Context,
        start_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter earlier entries.",
                default=None,
            ),
        ],
        end_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter later entries.",
                default=None,
            ),
        ],
        display: Annotated[
            str | None,
            Field(
                description="Display format. Leave blank or set to `full` or `parent`.",
                default=None,
            ),
        ],
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
                description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
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
        return await list_for_folder_history(
            context,
            start_at,
            end_at,
            display,
            cursor,
            per_page,
            sort_by,
            path,
            fields=fields,
        )

    @mcp.tool(
        name="List_For_User_History",
        description="List history for specific user.",
    )
    async def list_for_user_history_tool(
        context: Context,
        start_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter earlier entries.",
                default=None,
            ),
        ],
        end_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter later entries.",
                default=None,
            ),
        ],
        display: Annotated[
            str | None,
            Field(
                description="Display format. Leave blank or set to `full` or `parent`.",
                default=None,
            ),
        ],
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
                description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        user_id: Annotated[
            int | None, Field(description="User ID.", default=None)
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
        return await list_for_user_history(
            context,
            start_at,
            end_at,
            display,
            cursor,
            per_page,
            sort_by,
            user_id,
            fields=fields,
        )

    @mcp.tool(
        name="List_Logins_History", description="List site login history."
    )
    async def list_logins_history_tool(
        context: Context,
        start_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter earlier entries.",
                default=None,
            ),
        ],
        end_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter later entries.",
                default=None,
            ),
        ],
        display: Annotated[
            str | None,
            Field(
                description="Display format. Leave blank or set to `full` or `parent`.",
                default=None,
            ),
        ],
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
                description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
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
        return await list_logins_history(
            context,
            start_at,
            end_at,
            display,
            cursor,
            per_page,
            sort_by,
            fields=fields,
        )

    @mcp.tool(
        name="List_History", description="List site full action history."
    )
    async def list_history_tool(
        context: Context,
        start_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter earlier entries.",
                default=None,
            ),
        ],
        end_at: Annotated[
            str | None,
            Field(
                description="Leave blank or set to a date/time to filter later entries.",
                default=None,
            ),
        ],
        display: Annotated[
            str | None,
            Field(
                description="Display format. Leave blank or set to `full` or `parent`.",
                default=None,
            ),
        ],
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
                description="If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is equal to the supplied value. Valid fields are `user_id`, `folder` or `path`.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
        filter_prefix: Annotated[
            dict | None,
            Field(
                description="If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.",
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
        return await list_history(
            context,
            start_at,
            end_at,
            display,
            cursor,
            per_page,
            sort_by,
            filter,
            filter_prefix,
            fields=fields,
        )
