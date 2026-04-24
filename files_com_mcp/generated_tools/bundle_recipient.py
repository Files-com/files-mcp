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


async def list_bundle_recipient(
    context: Context,
    bundle_id: Annotated[
        int | None,
        Field(
            description="List recipients for the bundle with this ID.",
            default=None,
        ),
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
    """List Share Link Recipients

    Args:
        bundle_id: List recipients for the bundle with this ID.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if bundle_id is None:
            return "Missing required parameter: bundle_id"
        params["bundle_id"] = bundle_id

        list_obj = files_sdk.bundle_recipient.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No bundlerecipients found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "company",
                "name",
                "note",
                "recipient",
                "sent_at",
                "workspace_id",
            ],
            fields=fields,
        )
        response = f"BundleRecipient Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def create_bundle_recipient(
    context: Context,
    bundle_id: Annotated[
        int | None, Field(description="Bundle to share.", default=None)
    ],
    recipient: Annotated[
        str | None,
        Field(
            description="Email addresses to share this bundle with.",
            default=None,
        ),
    ],
    name: Annotated[
        str | None, Field(description="Name of recipient.", default=None)
    ],
    company: Annotated[
        str | None, Field(description="Company of recipient.", default=None)
    ],
    note: Annotated[
        str | None,
        Field(description="Note to include in email.", default=None),
    ],
) -> str:
    """Create Share Link Recipient

    Args:
        bundle_id: Bundle to share.
        recipient: Email addresses to share this bundle with.
        name: Name of recipient.
        company: Company of recipient.
        note: Note to include in email.
    """

    try:
        options = {"api_key": context_api_key(context)}
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
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "company",
                "name",
                "note",
                "recipient",
                "sent_at",
                "workspace_id",
            ],
        )
        response = f"BundleRecipient Response:\n{markdown_list}"
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
        name="List_Bundle_Recipient", description="List Share Link Recipients"
    )
    async def list_bundle_recipient_tool(
        context: Context,
        bundle_id: Annotated[
            int | None,
            Field(
                description="List recipients for the bundle with this ID.",
                default=None,
            ),
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
        return await list_bundle_recipient(context, bundle_id, fields=fields)

    @mcp.tool(
        name="Create_Bundle_Recipient",
        description="Create Share Link Recipient",
    )
    async def create_bundle_recipient_tool(
        context: Context,
        bundle_id: Annotated[
            int | None, Field(description="Bundle to share.", default=None)
        ],
        recipient: Annotated[
            str | None,
            Field(
                description="Email addresses to share this bundle with.",
                default=None,
            ),
        ],
        name: Annotated[
            str | None, Field(description="Name of recipient.", default=None)
        ],
        company: Annotated[
            str | None,
            Field(description="Company of recipient.", default=None),
        ],
        note: Annotated[
            str | None,
            Field(description="Note to include in email.", default=None),
        ],
    ) -> str:
        return await create_bundle_recipient(
            context, bundle_id, recipient, name, company, note
        )
