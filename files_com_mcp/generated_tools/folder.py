from fastmcp import Context
from fastmcp.exceptions import ToolError
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


async def list_for_folder(
    context: Context,
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
    ],
    cursor: Annotated[
        str | None,
        Field(
            description="Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.",
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
    """List Folders by Path

    Args:
        path: Path to operate on.
        cursor: Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
        per_page: Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """

    params = {}
    if path is None:
        raise ToolError("Missing required parameter: path")
    params["path"] = path
    if cursor is not None:
        params["cursor"] = cursor
    if per_page is not None:
        params["per_page"] = per_page

    def call(options):
        # One page; the response tells the caller how to fetch the next.
        page = files_sdk.folder.list_for(path, params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
    if not retval:
        return "No folders found."

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "path",
            "created_by_id",
            "created_by_api_key_id",
            "created_by_as2_incoming_message_id",
            "created_by_automation_id",
            "created_by_bundle_registration_id",
            "created_by_inbox_id",
            "created_by_remote_server_id",
            "created_by_sync_id",
            "custom_metadata",
            "display_name",
            "type",
            "size",
            "created_at",
            "last_modified_by_id",
            "last_modified_by_api_key_id",
            "last_modified_by_automation_id",
            "last_modified_by_bundle_registration_id",
            "last_modified_by_remote_server_id",
            "last_modified_by_sync_id",
            "mtime",
            "provided_mtime",
            "crc32",
            "md5",
            "sha1",
            "sha256",
            "mime_type",
            "region",
            "permissions",
            "subfolders_locked?",
            "is_locked",
            "download_uri",
            "direct_connection_info",
            "priority_color",
            "preview_id",
            "preview",
        ],
        fields=fields,
    )
    response = f"Folder Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


async def create_folder(
    context: Context,
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
    ],
) -> str:
    """Create Folder

    Args:
        path: Path to operate on.
    """

    params = {}
    if path is None:
        raise ToolError("Missing required parameter: path")
    params["path"] = path
    # Creating a nested folder also creates its missing parent directories.
    params["mkdir_parents"] = True

    def call(options):
        return [files_sdk.folder.create(path, params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        [
            "path",
            "created_by_id",
            "created_by_api_key_id",
            "created_by_as2_incoming_message_id",
            "created_by_automation_id",
            "created_by_bundle_registration_id",
            "created_by_inbox_id",
            "created_by_remote_server_id",
            "created_by_sync_id",
            "custom_metadata",
            "display_name",
            "type",
            "size",
            "created_at",
            "last_modified_by_id",
            "last_modified_by_api_key_id",
            "last_modified_by_automation_id",
            "last_modified_by_bundle_registration_id",
            "last_modified_by_remote_server_id",
            "last_modified_by_sync_id",
            "mtime",
            "provided_mtime",
            "crc32",
            "md5",
            "sha1",
            "sha256",
            "mime_type",
            "region",
            "permissions",
            "subfolders_locked?",
            "is_locked",
            "download_uri",
            "direct_connection_info",
            "priority_color",
            "preview_id",
            "preview",
        ],
    )
    response = f"Folder Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_For_Folder",
        description="List Folders by Path",
        annotations={
            "title": "List For Folder",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def list_for_folder_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
        cursor: Annotated[
            str | None,
            Field(
                description="Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.",
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
        return await list_for_folder(
            context, path, cursor, per_page, fields=fields
        )

    @mcp.tool(
        name="Create_Folder",
        description="Create Folder",
        annotations={
            "title": "Create Folder",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": False,
        },
    )
    async def create_folder_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
    ) -> str:
        return await create_folder(context, path)
