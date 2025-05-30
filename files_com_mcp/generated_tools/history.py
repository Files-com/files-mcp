from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_for_file_history(
    context: Context, path: str | None = None
) -> str:
    """List history for specific file.

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

        retval = files_sdk.history.list_for_file(path, params, options)
        retval = [item for item in retval.auto_paging_iter()]
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
        )
        return f"History Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_for_folder_history(
    context: Context, path: str | None = None
) -> str:
    """List history for specific folder.

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

        retval = files_sdk.history.list_for_folder(path, params, options)
        retval = [item for item in retval.auto_paging_iter()]
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
        )
        return f"History Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_for_user_history(
    context: Context, user_id: int | None = None
) -> str:
    """List history for specific user.

    Args:
        user_id: User ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if user_id is None:
            return "Missing required parameter: user_id"
        params["user_id"] = user_id

        retval = files_sdk.history.list_for_user(user_id, params, options)
        retval = [item for item in retval.auto_paging_iter()]
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
        )
        return f"History Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_logins_history(context: Context) -> str:
    """List site login history."""

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}

        retval = files_sdk.history.list_logins(params, options)
        retval = [item for item in retval.auto_paging_iter()]
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
        )
        return f"History Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def list_history(context: Context) -> str:
    """List site full action history."""

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}

        retval = files_sdk.history.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
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
        )
        return f"History Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_For_File_History")
    async def list_for_file_history_tool(
        context: Context, path: str | None = None
    ) -> str:
        return await list_for_file_history(context, path)

    @mcp.tool(name="List_For_Folder_History")
    async def list_for_folder_history_tool(
        context: Context, path: str | None = None
    ) -> str:
        return await list_for_folder_history(context, path)

    @mcp.tool(name="List_For_User_History")
    async def list_for_user_history_tool(
        context: Context, user_id: int | None = None
    ) -> str:
        return await list_for_user_history(context, user_id)

    @mcp.tool(name="List_Logins_History")
    async def list_logins_history_tool(context: Context) -> str:
        return await list_logins_history(context)

    @mcp.tool(name="List_History")
    async def list_history_tool(context: Context) -> str:
        return await list_history(context)
