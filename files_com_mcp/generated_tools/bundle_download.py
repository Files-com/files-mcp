from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_bundle_download(
    context: Context, bundle_id: int | None = None
) -> str:
    """List Bundle Downloads

    Args:
        bundle_id: Bundle ID
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if bundle_id is not None:
            params["bundle_id"] = bundle_id

        retval = files_sdk.bundle_download.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
        if not retval:
            return "No bundledownloads found."

        markdown_list = object_list_to_markdown_table(retval, ["bundle_id"])
        return f"BundleDownload Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_Bundle_Download")
    async def list_bundle_download_tool(
        context: Context, bundle_id: int | None = None
    ) -> str:
        return await list_bundle_download(context, bundle_id)
