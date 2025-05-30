from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_user(context: Context) -> str:
    """List Users"""

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}

        retval = files_sdk.user.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
        if not retval:
            return "No users found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "email",
                "group_ids",
                "password",
                "authentication_method",
                "name",
                "company",
                "notes",
                "require_password_change",
                "user_root",
                "user_home",
            ],
        )
        return f"User Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def find_user(context: Context, id: int | None = None) -> str:
    """Show User

    Args:
        id: User ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.user.find(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "email",
                "group_ids",
                "password",
                "authentication_method",
                "name",
                "company",
                "notes",
                "require_password_change",
                "user_root",
                "user_home",
            ],
        )
        return f"User Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def create_user(
    context: Context,
    username: str | None = None,
    email: str | None = None,
    group_ids: str | None = None,
    password: str | None = None,
    authentication_method: str | None = None,
    name: str | None = None,
    company: str | None = None,
    notes: str | None = None,
    require_password_change: bool | None = None,
    user_root: str | None = None,
    user_home: str | None = None,
) -> str:
    """Create User

    Args:
        username: User's username
        email: User's email.
        group_ids: A list of group ids to associate this user with.  Comma delimited.
        password: User password.
        authentication_method: How is this user authenticated?
        name: User's full name
        company: User's company
        notes: Any internal notes on the user
        require_password_change: Is a password change required upon next user login?
        user_root: Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set).  Note that this is not used for API, Desktop, or Web interface.
        user_home: Home folder for FTP/SFTP.  Note that this is not used for API, Desktop, or Web interface.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if username is None:
            return "Missing required parameter: username"
        params["username"] = username
        if email is not None:
            params["email"] = email
        if group_ids is not None:
            params["group_ids"] = group_ids
        if password is not None:
            params["password"] = password
        if authentication_method is not None:
            params["authentication_method"] = authentication_method
        if name is not None:
            params["name"] = name
        if company is not None:
            params["company"] = company
        if notes is not None:
            params["notes"] = notes
        if require_password_change is not None:
            params["require_password_change"] = require_password_change
        if user_root is not None:
            params["user_root"] = user_root
        if user_home is not None:
            params["user_home"] = user_home

        # Smart Default(s)
        params["dav_permission"] = True

        # Smart Default(s)
        params["ftp_permission"] = True

        # Smart Default(s)
        params["restapi_permission"] = True

        # Smart Default(s)
        params["sftp_permission"] = True

        retval = files_sdk.user.create(params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "email",
                "group_ids",
                "password",
                "authentication_method",
                "name",
                "company",
                "notes",
                "require_password_change",
                "user_root",
                "user_home",
            ],
        )
        return f"User Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def update_user(
    context: Context,
    id: int | None = None,
    email: str | None = None,
    group_ids: str | None = None,
    password: str | None = None,
    authentication_method: str | None = None,
    name: str | None = None,
    company: str | None = None,
    notes: str | None = None,
    require_password_change: bool | None = None,
    user_root: str | None = None,
    user_home: str | None = None,
    username: str | None = None,
) -> str:
    """Update User

    Args:
        id: User ID.
        email: User's email.
        group_ids: A list of group ids to associate this user with.  Comma delimited.
        password: User password.
        authentication_method: How is this user authenticated?
        name: User's full name
        company: User's company
        notes: Any internal notes on the user
        require_password_change: Is a password change required upon next user login?
        user_root: Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set).  Note that this is not used for API, Desktop, or Web interface.
        user_home: Home folder for FTP/SFTP.  Note that this is not used for API, Desktop, or Web interface.
        username: User's username
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id
        if email is not None:
            params["email"] = email
        if group_ids is not None:
            params["group_ids"] = group_ids
        if password is not None:
            params["password"] = password
        if authentication_method is not None:
            params["authentication_method"] = authentication_method
        if name is not None:
            params["name"] = name
        if company is not None:
            params["company"] = company
        if notes is not None:
            params["notes"] = notes
        if require_password_change is not None:
            params["require_password_change"] = require_password_change
        if user_root is not None:
            params["user_root"] = user_root
        if user_home is not None:
            params["user_home"] = user_home
        if username is not None:
            params["username"] = username

        # Smart Default(s)
        params["dav_permission"] = True

        # Smart Default(s)
        params["ftp_permission"] = True

        # Smart Default(s)
        params["restapi_permission"] = True

        # Smart Default(s)
        params["sftp_permission"] = True

        retval = files_sdk.user.update(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "email",
                "group_ids",
                "password",
                "authentication_method",
                "name",
                "company",
                "notes",
                "require_password_change",
                "user_root",
                "user_home",
            ],
        )
        return f"User Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def delete_user(context: Context, id: int | None = None) -> str:
    """Delete User

    Args:
        id: User ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.user.delete(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "email",
                "group_ids",
                "password",
                "authentication_method",
                "name",
                "company",
                "notes",
                "require_password_change",
                "user_root",
                "user_home",
            ],
        )
        return f"User Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_User")
    async def list_user_tool(context: Context) -> str:
        return await list_user(context)

    @mcp.tool(name="Find_User")
    async def find_user_tool(context: Context, id: int | None = None) -> str:
        return await find_user(context, id)

    @mcp.tool(name="Create_User")
    async def create_user_tool(
        context: Context,
        username: str | None = None,
        email: str | None = None,
        group_ids: str | None = None,
        password: str | None = None,
        authentication_method: str | None = None,
        name: str | None = None,
        company: str | None = None,
        notes: str | None = None,
        require_password_change: bool | None = None,
        user_root: str | None = None,
        user_home: str | None = None,
    ) -> str:
        return await create_user(
            context,
            username,
            email,
            group_ids,
            password,
            authentication_method,
            name,
            company,
            notes,
            require_password_change,
            user_root,
            user_home,
        )

    @mcp.tool(name="Update_User")
    async def update_user_tool(
        context: Context,
        id: int | None = None,
        email: str | None = None,
        group_ids: str | None = None,
        password: str | None = None,
        authentication_method: str | None = None,
        name: str | None = None,
        company: str | None = None,
        notes: str | None = None,
        require_password_change: bool | None = None,
        user_root: str | None = None,
        user_home: str | None = None,
        username: str | None = None,
    ) -> str:
        return await update_user(
            context,
            id,
            email,
            group_ids,
            password,
            authentication_method,
            name,
            company,
            notes,
            require_password_change,
            user_root,
            user_home,
            username,
        )

    @mcp.tool(name="Delete_User")
    async def delete_user_tool(context: Context, id: int | None = None) -> str:
        return await delete_user(context, id)
