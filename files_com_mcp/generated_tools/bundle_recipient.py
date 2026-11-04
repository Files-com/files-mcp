from fastmcp import Context
from fastmcp.exceptions import ToolError
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


async def list_bundle_recipient(
    context: Context,
    bundle_id: Annotated[
        int | None,
        Field(
            description="List recipients for the bundle with this ID.",
            default=None,
        ),
    ],
    cursor: Annotated[
        str | None,
        Field(
            description="Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.",
            default=None,
        ),
    ],
    per_page: Annotated[
        int | None,
        Field(
            description="Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).",
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
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """

    params = {}
    if bundle_id is None:
        raise ToolError("Missing required parameter: bundle_id")
    params["bundle_id"] = bundle_id
    if cursor is not None:
        params["cursor"] = cursor
    if per_page is not None:
        params["per_page"] = per_page

    def call(options):
        # One page; the response tells the caller how to fetch the next.
        page = files_sdk.bundle_recipient.list(params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
    if not retval:
        return "No bundlerecipients found."

    markdown_list = object_list_to_markdown_table(
        retval,
        ["company", "name", "note", "recipient", "sent_at", "workspace_id"],
        fields=fields,
    )
    response = f"BundleRecipient Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


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
    share_after_create: Annotated[
        bool | None,
        Field(
            description="Set to true to share the link with the recipient upon creation.",
            default=None,
        ),
    ],
) -> str:
    """Create Share Link Recipient

    Args:
        bundle_id: Bundle to share.
        recipient: Email addresses to share this bundle with.
        name: Name of recipient.
        company: Company of recipient.
        note: Note to include in email.
        share_after_create: Set to true to share the link with the recipient upon creation.
    """

    params = {}
    if bundle_id is None:
        raise ToolError("Missing required parameter: bundle_id")
    params["bundle_id"] = bundle_id
    if recipient is None:
        raise ToolError("Missing required parameter: recipient")
    params["recipient"] = recipient
    if name is not None:
        params["name"] = name
    if company is not None:
        params["company"] = company
    if note is not None:
        params["note"] = note
    if share_after_create is not None:
        params["share_after_create"] = share_after_create

    def call(options):
        return [files_sdk.bundle_recipient.create(params, options)], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(
        retval,
        ["company", "name", "note", "recipient", "sent_at", "workspace_id"],
    )
    response = f"BundleRecipient Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_Bundle_Recipient",
        description="List Share Link Recipients",
        annotations={
            "title": "List Bundle Recipient",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
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
        cursor: Annotated[
            str | None,
            Field(
                description="Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.",
                default=None,
            ),
        ],
        per_page: Annotated[
            int | None,
            Field(
                description="Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).",
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
        return await list_bundle_recipient(
            context, bundle_id, cursor, per_page, fields=fields
        )

    @mcp.tool(
        name="Create_Bundle_Recipient",
        description="Create Share Link Recipient",
        annotations={
            "title": "Create Bundle Recipient",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": False,
        },
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
        share_after_create: Annotated[
            bool | None,
            Field(
                description="Set to true to share the link with the recipient upon creation.",
                default=None,
            ),
        ],
    ) -> str:
        return await create_bundle_recipient(
            context,
            bundle_id,
            recipient,
            name,
            company,
            note,
            share_after_create,
        )
