from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import context_api_key, object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_for_folder(
    context: Context,
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
    ],
    fields: Annotated[
        list[str] | None,
        Field(
            description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
            default=None,
        ),
    ],
) -> str:
    """List Folders by Path

    Args:
        path: Path to operate on.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        list_obj = files_sdk.folder.list_for(path, params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
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
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


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

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        # Smart Default(s)
        params["mkdir_parents"] = True

        retval = files_sdk.folder.create(path, params, options)
        retval = [retval]
        next_cursor = None

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
                "priority_color",
                "preview_id",
                "preview",
            ],
        )
        response = f"Folder Response:\n{markdown_list}"
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
    @mcp.tool(name="List_For_Folder", description="List Folders by Path")
    async def list_for_folder_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
        fields: Annotated[
            list[str] | None,
            Field(
                description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
                default=None,
            ),
        ],
    ) -> str:
        return await list_for_folder(context, path, fields=fields)

    @mcp.tool(name="Create_Folder", description="Create Folder")
    async def create_folder_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
    ) -> str:
        return await create_folder(context, path)
