from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import context_api_key, object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_bundle_download(
    context: Context,
    bundle_id: Annotated[
        int | None, Field(description="Bundle ID", default=None)
    ],
    fields: Annotated[
        list[str] | None,
        Field(
            description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
            default=None,
        ),
    ],
) -> str:
    """List Share Link Downloads

    Args:
        bundle_id: Bundle ID
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if bundle_id is not None:
            params["bundle_id"] = bundle_id

        list_obj = files_sdk.bundle_download.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No bundledownloads found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "bundle_registration",
                "download_method",
                "path",
                "workspace_id",
                "created_at",
            ],
            fields=fields,
        )
        response = f"BundleDownload Response:\n{markdown_list}"
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
        name="List_Bundle_Download", description="List Share Link Downloads"
    )
    async def list_bundle_download_tool(
        context: Context,
        bundle_id: Annotated[
            int | None, Field(description="Bundle ID", default=None)
        ],
        fields: Annotated[
            list[str] | None,
            Field(
                description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
                default=None,
            ),
        ],
    ) -> str:
        return await list_bundle_download(context, bundle_id, fields=fields)
