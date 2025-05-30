import os
from fastmcp import Context
import files_sdk
import files_sdk.error


async def download_file_to_local(
    context: Context, remote_path: str, local_path: str
) -> str:
    """Download a file from my Files.com site. Specify the remote path of the file to download and a local path to save the file at.

    Args:
        remote_path: The full path on my Files.com site of the file to be downloaded.
        local_path: The full path on my local system to save the downloaded file to. Must be a path that can be written to. When in doubt, use the `$HOME/Downloads` folder, or the `/tmp/` folder, as the destination for the downloaded file.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }

        files_sdk.file.download_file(remote_path, local_path, options)
        return (
            f"File downloaded successfully to: {os.path.abspath(local_path)}"
        )

    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def upload_file_from_local(
    context: Context, local_path: str, remote_path: str
) -> str:
    """Upload a file to my Files.com site. Specify the local path of the file to upload and a remote path to save the file at.

    Args:
        local_path: The full path on my local system of the file to be uploaded.
        remote_path: The full path on my Files.com site for the file to be uploaded to.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}

        # Smart Default(s)
        params["mkdir_parents"] = True

        files_sdk.file.upload_file(local_path, remote_path, options, params)
        return (
            f"File uploaded successfully from: {os.path.abspath(local_path)}"
        )

    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="Download_File_to_Local")
    async def download_file_to_local_tool(
        context: Context, remote_path: str, local_path: str
    ) -> str:
        return await download_file_to_local(context, remote_path, local_path)

    @mcp.tool(name="Upload_File_from_Local")
    async def upload_file_from_local_tool(
        context: Context,
        local_path: str,
        remote_path: str,
    ) -> str:
        return await upload_file_from_local(context, local_path, remote_path)
