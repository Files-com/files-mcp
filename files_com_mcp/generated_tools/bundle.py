from fastmcp import Context
from typing_extensions import Annotated
from pydantic import Field
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_bundle(context: Context) -> str:
    """List Bundles"""

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}

        retval = files_sdk.bundle.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
        if not retval:
            return "No bundles found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "paths",
                "password",
                "expires_at",
                "max_uses",
                "description",
                "note",
                "require_registration",
            ],
        )
        return f"Bundle Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def find_bundle(
    context: Context,
    id: Annotated[int | None, Field(description="Bundle ID.", default=None)],
) -> str:
    """Show Bundle (also called Share Link)

    Args:
        id: Bundle ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.bundle.find(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "paths",
                "password",
                "expires_at",
                "max_uses",
                "description",
                "note",
                "require_registration",
            ],
        )
        return f"Bundle Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def create_bundle(
    context: Context,
    paths: Annotated[
        list | None,
        Field(
            description="A list of paths to include in this bundle.",
            default=None,
        ),
    ],
    password: Annotated[
        str | None,
        Field(description="Password for this bundle.", default=None),
    ],
    expires_at: Annotated[
        str | None,
        Field(description="Bundle expiration date/time", default=None),
    ],
    max_uses: Annotated[
        int | None,
        Field(
            description="Maximum number of times bundle can be accessed",
            default=None,
        ),
    ],
    description: Annotated[
        str | None, Field(description="Public description", default=None)
    ],
    note: Annotated[
        str | None, Field(description="Bundle internal note", default=None)
    ],
    require_registration: Annotated[
        bool | None,
        Field(
            description="Show a registration page that captures the downloader's name and email address?",
            default=None,
        ),
    ],
) -> str:
    """Create Bundle (also called Share Link)

    Args:
        paths: A list of paths to include in this bundle.
        password: Password for this bundle.
        expires_at: Bundle expiration date/time
        max_uses: Maximum number of times bundle can be accessed
        description: Public description
        note: Bundle internal note
        require_registration: Show a registration page that captures the downloader's name and email address?
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if paths is None:
            return "Missing required parameter: paths"
        params["paths"] = paths
        if password is not None:
            params["password"] = password
        if expires_at is not None:
            params["expires_at"] = expires_at
        if max_uses is not None:
            params["max_uses"] = max_uses
        if description is not None:
            params["description"] = description
        if note is not None:
            params["note"] = note
        if require_registration is not None:
            params["require_registration"] = require_registration

        # Smart Default(s)
        params["permissions"] = "read"

        retval = files_sdk.bundle.create(params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "paths",
                "password",
                "expires_at",
                "max_uses",
                "description",
                "note",
                "require_registration",
            ],
        )
        return f"Bundle Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def update_bundle(
    context: Context,
    id: Annotated[int | None, Field(description="Bundle ID.", default=None)],
    expires_at: Annotated[
        str | None,
        Field(description="Bundle expiration date/time", default=None),
    ],
) -> str:
    """Update Bundle (also called Share Link)

    Args:
        id: Bundle ID.
        expires_at: Bundle expiration date/time
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id
        if expires_at is not None:
            params["expires_at"] = expires_at

        retval = files_sdk.bundle.update(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "paths",
                "password",
                "expires_at",
                "max_uses",
                "description",
                "note",
                "require_registration",
            ],
        )
        return f"Bundle Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def delete_bundle(
    context: Context,
    id: Annotated[int | None, Field(description="Bundle ID.", default=None)],
) -> str:
    """Delete Bundle (also called Share Link)

    Args:
        id: Bundle ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.bundle.delete(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "paths",
                "password",
                "expires_at",
                "max_uses",
                "description",
                "note",
                "require_registration",
            ],
        )
        return f"Bundle Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(
        name="List_Bundle",
        description="List Bundles (also called Share Links)",
    )
    async def list_bundle_tool(context: Context) -> str:
        return await list_bundle(context)

    @mcp.tool(
        name="Find_Bundle", description="Show Bundle (also called Share Link)"
    )
    async def find_bundle_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Bundle ID.", default=None)
        ],
    ) -> str:
        return await find_bundle(context, id)

    @mcp.tool(
        name="Create_Bundle",
        description="Create Bundle (also called Share Link)",
    )
    async def create_bundle_tool(
        context: Context,
        paths: Annotated[
            list | None,
            Field(
                description="A list of paths to include in this bundle.",
                default=None,
            ),
        ],
        password: Annotated[
            str | None,
            Field(description="Password for this bundle.", default=None),
        ],
        expires_at: Annotated[
            str | None,
            Field(description="Bundle expiration date/time", default=None),
        ],
        max_uses: Annotated[
            int | None,
            Field(
                description="Maximum number of times bundle can be accessed",
                default=None,
            ),
        ],
        description: Annotated[
            str | None, Field(description="Public description", default=None)
        ],
        note: Annotated[
            str | None, Field(description="Bundle internal note", default=None)
        ],
        require_registration: Annotated[
            bool | None,
            Field(
                description="Show a registration page that captures the downloader's name and email address?",
                default=None,
            ),
        ],
    ) -> str:
        return await create_bundle(
            context,
            paths,
            password,
            expires_at,
            max_uses,
            description,
            note,
            require_registration,
        )

    @mcp.tool(
        name="Update_Bundle",
        description="Update Bundle (also called Share Link)",
    )
    async def update_bundle_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Bundle ID.", default=None)
        ],
        expires_at: Annotated[
            str | None,
            Field(description="Bundle expiration date/time", default=None),
        ],
    ) -> str:
        return await update_bundle(context, id, expires_at)

    @mcp.tool(
        name="Delete_Bundle",
        description="Delete Bundle (also called Share Link)",
    )
    async def delete_bundle_tool(
        context: Context,
        id: Annotated[
            int | None, Field(description="Bundle ID.", default=None)
        ],
    ) -> str:
        return await delete_bundle(context, id)
