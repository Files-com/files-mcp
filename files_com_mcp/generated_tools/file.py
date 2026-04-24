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


async def delete_file(
    context: Context,
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
    ],
) -> str:
    """Delete File/Folder

    Args:
        path: Path to operate on.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        retval = files_sdk.file.delete(path, params, options)
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
        response = f"File Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def find_file(
    context: Context,
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
    ],
) -> str:
    """Find File/Folder by Path

    Args:
        path: Path to operate on.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        retval = files_sdk.file.find(path, params, options)
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
        response = f"File Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def zip_list_contents_file(
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
        BeforeValidator(coerce_json),
    ],
) -> str:
    """List the contents of a ZIP file.

    Args:
        path: Path to operate on.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        retval = files_sdk.file.zip_list_contents(path, params, options)
        next_cursor = None
        if not retval:
            return "No fileactions found."

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
        response = f"File Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def copy_file(
    context: Context,
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
    ],
    destination: Annotated[
        str | None, Field(description="Copy destination path.", default=None)
    ],
) -> str:
    """Copy File/Folder

    Args:
        path: Path to operate on.
        destination: Copy destination path.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path
        if destination is None:
            return "Missing required parameter: destination"
        params["destination"] = destination

        retval = files_sdk.file.copy(path, params, options)
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
        response = f"File Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def move_file(
    context: Context,
    path: Annotated[
        str | None, Field(description="Path to operate on.", default=None)
    ],
    destination: Annotated[
        str | None, Field(description="Move destination path.", default=None)
    ],
) -> str:
    """Move File/Folder

    Args:
        path: Path to operate on.
        destination: Move destination path.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path
        if destination is None:
            return "Missing required parameter: destination"
        params["destination"] = destination

        retval = files_sdk.file.move(path, params, options)
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
        response = f"File Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def unzip_file(
    context: Context,
    path: Annotated[
        str | None,
        Field(description="ZIP file path to extract.", default=None),
    ],
    destination: Annotated[
        str | None,
        Field(
            description="Destination folder path for extracted files.",
            default=None,
        ),
    ],
) -> str:
    """Extract a ZIP file to a destination folder.

    Args:
        path: ZIP file path to extract.
        destination: Destination folder path for extracted files.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path
        if destination is None:
            return "Missing required parameter: destination"
        params["destination"] = destination

        retval = files_sdk.file.unzip(path, params, options)
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
        response = f"File Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def zip_file(
    context: Context,
    paths: Annotated[
        list | None,
        Field(description="Paths to include in the ZIP.", default=None),
        BeforeValidator(coerce_json),
    ],
    destination: Annotated[
        str | None,
        Field(description="Destination file path for the ZIP.", default=None),
    ],
) -> str:
    """Create a ZIP from one or more paths and save it to a destination path.

    Args:
        paths: Paths to include in the ZIP.
        destination: Destination file path for the ZIP.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if paths is None:
            return "Missing required parameter: paths"
        params["paths"] = paths
        if destination is None:
            return "Missing required parameter: destination"
        params["destination"] = destination

        retval = files_sdk.file.zip(params, options)
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
        response = f"File Response:\n{markdown_list}"
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
    @mcp.tool(name="Delete_File", description="Delete File/Folder")
    async def delete_file_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
    ) -> str:
        return await delete_file(context, path)

    @mcp.tool(name="Find_File", description="Find File/Folder by Path")
    async def find_file_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
    ) -> str:
        return await find_file(context, path)

    @mcp.tool(
        name="Zip_List_Contents_File",
        description="List the contents of a ZIP file.",
    )
    async def zip_list_contents_file_tool(
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
            BeforeValidator(coerce_json),
        ],
    ) -> str:
        return await zip_list_contents_file(context, path, fields=fields)

    @mcp.tool(name="Copy_File", description="Copy File/Folder")
    async def copy_file_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
        destination: Annotated[
            str | None,
            Field(description="Copy destination path.", default=None),
        ],
    ) -> str:
        return await copy_file(context, path, destination)

    @mcp.tool(name="Move_File", description="Move File/Folder")
    async def move_file_tool(
        context: Context,
        path: Annotated[
            str | None, Field(description="Path to operate on.", default=None)
        ],
        destination: Annotated[
            str | None,
            Field(description="Move destination path.", default=None),
        ],
    ) -> str:
        return await move_file(context, path, destination)

    @mcp.tool(
        name="Unzip_File",
        description="Extract a ZIP file to a destination folder.",
    )
    async def unzip_file_tool(
        context: Context,
        path: Annotated[
            str | None,
            Field(description="ZIP file path to extract.", default=None),
        ],
        destination: Annotated[
            str | None,
            Field(
                description="Destination folder path for extracted files.",
                default=None,
            ),
        ],
    ) -> str:
        return await unzip_file(context, path, destination)

    @mcp.tool(
        name="Zip_File",
        description="Create a ZIP from one or more paths and save it to a destination path.",
    )
    async def zip_file_tool(
        context: Context,
        paths: Annotated[
            list | None,
            Field(description="Paths to include in the ZIP.", default=None),
            BeforeValidator(coerce_json),
        ],
        destination: Annotated[
            str | None,
            Field(
                description="Destination file path for the ZIP.", default=None
            ),
        ],
    ) -> str:
        return await zip_file(context, paths, destination)
