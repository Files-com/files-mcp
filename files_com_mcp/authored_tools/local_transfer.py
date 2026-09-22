import os
from pathlib import Path
from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import context_api_key
from files_com_mcp.local_paths import (
    LocalPathError,
    configured_local_root,
    resolve_local_path,
)
import files_sdk
import files_sdk.error


async def download_file_to_local(
    context: Context,
    remote_path: str,
    local_path: str,
    local_root: Path | None,
) -> str:
    """Download a file from my Files.com site. Specify the remote path of the file to download and a local path to save the file at.

    Args:
        remote_path: The full path on my Files.com site of the file to be downloaded.
        local_path: The path on my local system to save the downloaded file to.
        local_root: The configured local directory restriction, if any.
    """

    try:
        local_path = resolve_local_path(local_path, local_root)
        options = {"api_key": context_api_key(context)}

        files_sdk.file.download_file(remote_path, local_path, options)
        return (
            f"File downloaded successfully to: {os.path.abspath(local_path)}"
        )

    except LocalPathError as err:
        return f"Local Path Error: {err}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def upload_file_from_local(
    context: Context,
    local_path: str,
    remote_path: str,
    local_root: Path | None,
) -> str:
    """Upload a file to my Files.com site. Specify the local path of the file to upload and a remote path to save the file at.

    Args:
        local_path: The full path on my local system of the file to be uploaded.
        remote_path: The full path on my Files.com site for the file to be uploaded to.
        local_root: The configured local directory restriction, if any.
    """

    try:
        local_path = resolve_local_path(local_path, local_root)
        options = {"api_key": context_api_key(context)}
        params = {}

        # Smart Default(s)
        params["mkdir_parents"] = True

        files_sdk.file.upload_file(local_path, remote_path, options, params)
        return (
            f"File uploaded successfully from: {os.path.abspath(local_path)}"
        )

    except LocalPathError as err:
        return f"Local Path Error: {err}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    local_root = configured_local_root()
    download_path_description = (
        "The full path on my local system to save the downloaded file to. "
        "Must be a path that can be written to."
    )
    upload_path_description = (
        "The full path on my local system of the file to be uploaded."
    )
    if local_root is not None:
        restriction = (
            f" Must resolve within {local_root} or its subdirectories."
        )
        download_path_description += restriction
        upload_path_description += restriction
    else:
        download_path_description += (
            " When in doubt, use the `$HOME/Downloads` folder, or the `/tmp/` "
            "folder, as the destination for the downloaded file."
        )

    @mcp.tool(
        name="Download_File_to_Local",
        description="Download a file from my Files.com site.",
        annotations={
            "title": "Download File to Local",
            "readOnlyHint": False,
            "destructiveHint": True,
            "openWorldHint": False,
        },
    )
    async def download_file_to_local_tool(
        context: Context,
        remote_path: Annotated[
            str,
            Field(
                description="The full path on my Files.com site of the file to be downloaded."
            ),
        ],
        local_path: Annotated[
            str,
            Field(description=download_path_description),
        ],
    ) -> str:
        return await download_file_to_local(
            context, remote_path, local_path, local_root
        )

    @mcp.tool(
        name="Upload_File_from_Local",
        description="Upload a file to my Files.com site.",
        annotations={
            "title": "Upload File from Local",
            "readOnlyHint": False,
            "destructiveHint": True,
            "openWorldHint": False,
        },
    )
    async def upload_file_from_local_tool(
        context: Context,
        local_path: Annotated[
            str,
            Field(description=upload_path_description),
        ],
        remote_path: Annotated[
            str,
            Field(
                description="The full path on my Files.com site for the file to be uploaded to."
            ),
        ],
    ) -> str:
        return await upload_file_from_local(
            context, local_path, remote_path, local_root
        )
