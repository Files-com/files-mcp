from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import object_list_to_markdown_table
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
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        retval = files_sdk.file.delete(path, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["path", "destination"]
        )
        return f"File Response:\n{markdown_list}"
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
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path

        retval = files_sdk.file.find(path, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["path", "destination"]
        )
        return f"File Response:\n{markdown_list}"
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
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path
        if destination is None:
            return "Missing required parameter: destination"
        params["destination"] = destination

        retval = files_sdk.file.copy(path, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["path", "destination"]
        )
        return f"File Response:\n{markdown_list}"
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
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if path is None:
            return "Missing required parameter: path"
        params["path"] = path
        if destination is None:
            return "Missing required parameter: destination"
        params["destination"] = destination

        retval = files_sdk.file.move(path, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["path", "destination"]
        )
        return f"File Response:\n{markdown_list}"
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
