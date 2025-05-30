from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_bundle_recipient(
    context: Context, bundle_id: int | None = None
) -> str:
    """List Bundle Recipients

    Args:
        bundle_id: List recipients for the bundle with this ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if bundle_id is None:
            return "Missing required parameter: bundle_id"
        params["bundle_id"] = bundle_id

        retval = files_sdk.bundle_recipient.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
        if not retval:
            return "No bundlerecipients found."

        markdown_list = object_list_to_markdown_table(
            retval, ["bundle_id", "recipient", "name", "company", "note"]
        )
        return f"BundleRecipient Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def create_bundle_recipient(
    context: Context,
    bundle_id: int | None = None,
    recipient: str | None = None,
    name: str | None = None,
    company: str | None = None,
    note: str | None = None,
) -> str:
    """Create Bundle Recipient

    Args:
        bundle_id: Bundle to share.
        recipient: Email addresses to share this bundle with.
        name: Name of recipient.
        company: Company of recipient.
        note: Note to include in email.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if bundle_id is None:
            return "Missing required parameter: bundle_id"
        params["bundle_id"] = bundle_id
        if recipient is None:
            return "Missing required parameter: recipient"
        params["recipient"] = recipient
        if name is not None:
            params["name"] = name
        if company is not None:
            params["company"] = company
        if note is not None:
            params["note"] = note

        # Smart Default(s)
        params["share_after_create"] = True

        retval = files_sdk.bundle_recipient.create(params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval, ["bundle_id", "recipient", "name", "company", "note"]
        )
        return f"BundleRecipient Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_Bundle_Recipient")
    async def list_bundle_recipient_tool(
        context: Context, bundle_id: int | None = None
    ) -> str:
        return await list_bundle_recipient(context, bundle_id)

    @mcp.tool(name="Create_Bundle_Recipient")
    async def create_bundle_recipient_tool(
        context: Context,
        bundle_id: int | None = None,
        recipient: str | None = None,
        name: str | None = None,
        company: str | None = None,
        note: str | None = None,
    ) -> str:
        return await create_bundle_recipient(
            context, bundle_id, recipient, name, company, note
        )
