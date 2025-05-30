from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def delete_file(context: Context, path: str | None = None) -> str:
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


async def find_file(context: Context, path: str | None = None) -> str:
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
    context: Context, path: str | None = None, destination: str | None = None
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
    context: Context, path: str | None = None, destination: str | None = None
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
    @mcp.tool(name="Delete_File")
    async def delete_file_tool(
        context: Context, path: str | None = None
    ) -> str:
        return await delete_file(context, path)

    @mcp.tool(name="Find_File")
    async def find_file_tool(context: Context, path: str | None = None) -> str:
        return await find_file(context, path)

    @mcp.tool(name="Copy_File")
    async def copy_file_tool(
        context: Context,
        path: str | None = None,
        destination: str | None = None,
    ) -> str:
        return await copy_file(context, path, destination)

    @mcp.tool(name="Move_File")
    async def move_file_tool(
        context: Context,
        path: str | None = None,
        destination: str | None = None,
    ) -> str:
        return await move_file(context, path, destination)
