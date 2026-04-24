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


async def list_user(
    context: Context,
    fields: Annotated[
        list[str] | None,
        Field(
            description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
            default=None,
        ),
        BeforeValidator(coerce_json),
    ],
) -> str:
    """List Users"""

    try:
        options = {"api_key": context_api_key(context)}
        params = {}

        list_obj = files_sdk.user.list(params, options)
        retval = list(list_obj)
        next_cursor = getattr(list_obj, "cursor", None)
        if not retval:
            return "No users found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "admin_group_ids",
                "allowed_ips",
                "attachments_permission",
                "api_keys_count",
                "authenticate_until",
                "authentication_method",
                "avatar_url",
                "billable",
                "billing_permission",
                "bypass_site_allowed_ips",
                "bypass_user_lifecycle_rules",
                "created_at",
                "dav_permission",
                "disabled",
                "disabled_expired_or_inactive",
                "desktop_configuration_profile_id",
                "email",
                "filesystem_layout",
                "first_login_at",
                "ftp_permission",
                "group_ids",
                "header_text",
                "language",
                "last_login_at",
                "last_web_login_at",
                "last_ftp_login_at",
                "last_sftp_login_at",
                "last_dav_login_at",
                "last_desktop_login_at",
                "last_restapi_login_at",
                "last_api_use_at",
                "last_active_at",
                "last_protocol_cipher",
                "lockout_expires",
                "name",
                "company",
                "notes",
                "notification_daily_send_time",
                "office_integration_enabled",
                "partner_admin",
                "partner_id",
                "partner_name",
                "password_set_at",
                "password_validity_days",
                "primary_group_id",
                "public_keys_count",
                "receive_admin_alerts",
                "require_2fa",
                "require_login_by",
                "active_2fa",
                "require_password_change",
                "password_expired",
                "readonly_site_admin",
                "restapi_permission",
                "self_managed",
                "sftp_permission",
                "site_admin",
                "workspace_admin",
                "site_id",
                "workspace_id",
                "skip_welcome_screen",
                "ssl_required",
                "sso_strategy_id",
                "subscribe_to_newsletter",
                "externally_managed",
                "tags",
                "time_zone",
                "type_of_2fa",
                "type_of_2fa_for_display",
                "user_root",
                "user_home",
                "days_remaining_until_password_expire",
                "password_expire_at",
            ],
            fields=fields,
        )
        response = f"User Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def find_user(
    context: Context,
    id: Annotated[int | None, Field(description="User ID.", default=None)],
) -> str:
    """Show User

    Args:
        id: User ID.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.user.find(id, params, options)
        retval = [retval]
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "admin_group_ids",
                "allowed_ips",
                "attachments_permission",
                "api_keys_count",
                "authenticate_until",
                "authentication_method",
                "avatar_url",
                "billable",
                "billing_permission",
                "bypass_site_allowed_ips",
                "bypass_user_lifecycle_rules",
                "created_at",
                "dav_permission",
                "disabled",
                "disabled_expired_or_inactive",
                "desktop_configuration_profile_id",
                "email",
                "filesystem_layout",
                "first_login_at",
                "ftp_permission",
                "group_ids",
                "header_text",
                "language",
                "last_login_at",
                "last_web_login_at",
                "last_ftp_login_at",
                "last_sftp_login_at",
                "last_dav_login_at",
                "last_desktop_login_at",
                "last_restapi_login_at",
                "last_api_use_at",
                "last_active_at",
                "last_protocol_cipher",
                "lockout_expires",
                "name",
                "company",
                "notes",
                "notification_daily_send_time",
                "office_integration_enabled",
                "partner_admin",
                "partner_id",
                "partner_name",
                "password_set_at",
                "password_validity_days",
                "primary_group_id",
                "public_keys_count",
                "receive_admin_alerts",
                "require_2fa",
                "require_login_by",
                "active_2fa",
                "require_password_change",
                "password_expired",
                "readonly_site_admin",
                "restapi_permission",
                "self_managed",
                "sftp_permission",
                "site_admin",
                "workspace_admin",
                "site_id",
                "workspace_id",
                "skip_welcome_screen",
                "ssl_required",
                "sso_strategy_id",
                "subscribe_to_newsletter",
                "externally_managed",
                "tags",
                "time_zone",
                "type_of_2fa",
                "type_of_2fa_for_display",
                "user_root",
                "user_home",
                "days_remaining_until_password_expire",
                "password_expire_at",
            ],
        )
        response = f"User Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def create_user(
    context: Context,
    username: Annotated[
        str | None, Field(description="User's username", default=None)
    ],
    email: Annotated[
        str | None, Field(description="User's email.", default=None)
    ],
    group_ids: Annotated[
        str | None,
        Field(
            description="A list of group ids to associate this user with.  Comma delimited.",
            default=None,
        ),
    ],
    password: Annotated[
        str | None, Field(description="User password.", default=None)
    ],
    authentication_method: Annotated[
        str | None,
        Field(description="How is this user authenticated?", default=None),
    ],
    name: Annotated[
        str | None, Field(description="User's full name", default=None)
    ],
    company: Annotated[
        str | None, Field(description="User's company", default=None)
    ],
    notes: Annotated[
        str | None,
        Field(description="Any internal notes on the user", default=None),
    ],
    require_password_change: Annotated[
        bool | None,
        Field(
            description="Is a password change required upon next user login?",
            default=None,
        ),
    ],
    user_root: Annotated[
        str | None,
        Field(
            description="Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set).  Note that this is not used for API, Desktop, or Web interface.",
            default=None,
        ),
    ],
    user_home: Annotated[
        str | None,
        Field(
            description="Home folder for FTP/SFTP.  Note that this is not used for API, Desktop, or Web interface.",
            default=None,
        ),
    ],
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
        options = {"api_key": context_api_key(context)}
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
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "admin_group_ids",
                "allowed_ips",
                "attachments_permission",
                "api_keys_count",
                "authenticate_until",
                "authentication_method",
                "avatar_url",
                "billable",
                "billing_permission",
                "bypass_site_allowed_ips",
                "bypass_user_lifecycle_rules",
                "created_at",
                "dav_permission",
                "disabled",
                "disabled_expired_or_inactive",
                "desktop_configuration_profile_id",
                "email",
                "filesystem_layout",
                "first_login_at",
                "ftp_permission",
                "group_ids",
                "header_text",
                "language",
                "last_login_at",
                "last_web_login_at",
                "last_ftp_login_at",
                "last_sftp_login_at",
                "last_dav_login_at",
                "last_desktop_login_at",
                "last_restapi_login_at",
                "last_api_use_at",
                "last_active_at",
                "last_protocol_cipher",
                "lockout_expires",
                "name",
                "company",
                "notes",
                "notification_daily_send_time",
                "office_integration_enabled",
                "partner_admin",
                "partner_id",
                "partner_name",
                "password_set_at",
                "password_validity_days",
                "primary_group_id",
                "public_keys_count",
                "receive_admin_alerts",
                "require_2fa",
                "require_login_by",
                "active_2fa",
                "require_password_change",
                "password_expired",
                "readonly_site_admin",
                "restapi_permission",
                "self_managed",
                "sftp_permission",
                "site_admin",
                "workspace_admin",
                "site_id",
                "workspace_id",
                "skip_welcome_screen",
                "ssl_required",
                "sso_strategy_id",
                "subscribe_to_newsletter",
                "externally_managed",
                "tags",
                "time_zone",
                "type_of_2fa",
                "type_of_2fa_for_display",
                "user_root",
                "user_home",
                "days_remaining_until_password_expire",
                "password_expire_at",
            ],
        )
        response = f"User Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def update_user(
    context: Context,
    id: Annotated[int | None, Field(description="User ID.", default=None)],
    email: Annotated[
        str | None, Field(description="User's email.", default=None)
    ],
    group_ids: Annotated[
        str | None,
        Field(
            description="A list of group ids to associate this user with.  Comma delimited.",
            default=None,
        ),
    ],
    password: Annotated[
        str | None, Field(description="User password.", default=None)
    ],
    authentication_method: Annotated[
        str | None,
        Field(description="How is this user authenticated?", default=None),
    ],
    name: Annotated[
        str | None, Field(description="User's full name", default=None)
    ],
    company: Annotated[
        str | None, Field(description="User's company", default=None)
    ],
    notes: Annotated[
        str | None,
        Field(description="Any internal notes on the user", default=None),
    ],
    require_password_change: Annotated[
        bool | None,
        Field(
            description="Is a password change required upon next user login?",
            default=None,
        ),
    ],
    user_root: Annotated[
        str | None,
        Field(
            description="Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set).  Note that this is not used for API, Desktop, or Web interface.",
            default=None,
        ),
    ],
    user_home: Annotated[
        str | None,
        Field(
            description="Home folder for FTP/SFTP.  Note that this is not used for API, Desktop, or Web interface.",
            default=None,
        ),
    ],
    username: Annotated[
        str | None, Field(description="User's username", default=None)
    ],
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
        options = {"api_key": context_api_key(context)}
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
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "admin_group_ids",
                "allowed_ips",
                "attachments_permission",
                "api_keys_count",
                "authenticate_until",
                "authentication_method",
                "avatar_url",
                "billable",
                "billing_permission",
                "bypass_site_allowed_ips",
                "bypass_user_lifecycle_rules",
                "created_at",
                "dav_permission",
                "disabled",
                "disabled_expired_or_inactive",
                "desktop_configuration_profile_id",
                "email",
                "filesystem_layout",
                "first_login_at",
                "ftp_permission",
                "group_ids",
                "header_text",
                "language",
                "last_login_at",
                "last_web_login_at",
                "last_ftp_login_at",
                "last_sftp_login_at",
                "last_dav_login_at",
                "last_desktop_login_at",
                "last_restapi_login_at",
                "last_api_use_at",
                "last_active_at",
                "last_protocol_cipher",
                "lockout_expires",
                "name",
                "company",
                "notes",
                "notification_daily_send_time",
                "office_integration_enabled",
                "partner_admin",
                "partner_id",
                "partner_name",
                "password_set_at",
                "password_validity_days",
                "primary_group_id",
                "public_keys_count",
                "receive_admin_alerts",
                "require_2fa",
                "require_login_by",
                "active_2fa",
                "require_password_change",
                "password_expired",
                "readonly_site_admin",
                "restapi_permission",
                "self_managed",
                "sftp_permission",
                "site_admin",
                "workspace_admin",
                "site_id",
                "workspace_id",
                "skip_welcome_screen",
                "ssl_required",
                "sso_strategy_id",
                "subscribe_to_newsletter",
                "externally_managed",
                "tags",
                "time_zone",
                "type_of_2fa",
                "type_of_2fa_for_display",
                "user_root",
                "user_home",
                "days_remaining_until_password_expire",
                "password_expire_at",
            ],
        )
        response = f"User Response:\n{markdown_list}"
        if next_cursor:
            response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
        return response
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def delete_user(
    context: Context,
    id: Annotated[int | None, Field(description="User ID.", default=None)],
) -> str:
    """Delete User

    Args:
        id: User ID.
    """

    try:
        options = {"api_key": context_api_key(context)}
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.user.delete(id, params, options)
        retval = [retval]
        next_cursor = None

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "username",
                "admin_group_ids",
                "allowed_ips",
                "attachments_permission",
                "api_keys_count",
                "authenticate_until",
                "authentication_method",
                "avatar_url",
                "billable",
                "billing_permission",
                "bypass_site_allowed_ips",
                "bypass_user_lifecycle_rules",
                "created_at",
                "dav_permission",
                "disabled",
                "disabled_expired_or_inactive",
                "desktop_configuration_profile_id",
                "email",
                "filesystem_layout",
                "first_login_at",
                "ftp_permission",
                "group_ids",
                "header_text",
                "language",
                "last_login_at",
                "last_web_login_at",
                "last_ftp_login_at",
                "last_sftp_login_at",
                "last_dav_login_at",
                "last_desktop_login_at",
                "last_restapi_login_at",
                "last_api_use_at",
                "last_active_at",
                "last_protocol_cipher",
                "lockout_expires",
                "name",
                "company",
                "notes",
                "notification_daily_send_time",
                "office_integration_enabled",
                "partner_admin",
                "partner_id",
                "partner_name",
                "password_set_at",
                "password_validity_days",
                "primary_group_id",
                "public_keys_count",
                "receive_admin_alerts",
                "require_2fa",
                "require_login_by",
                "active_2fa",
                "require_password_change",
                "password_expired",
                "readonly_site_admin",
                "restapi_permission",
                "self_managed",
                "sftp_permission",
                "site_admin",
                "workspace_admin",
                "site_id",
                "workspace_id",
                "skip_welcome_screen",
                "ssl_required",
                "sso_strategy_id",
                "subscribe_to_newsletter",
                "externally_managed",
                "tags",
                "time_zone",
                "type_of_2fa",
                "type_of_2fa_for_display",
                "user_root",
                "user_home",
                "days_remaining_until_password_expire",
                "password_expire_at",
            ],
        )
        response = f"User Response:\n{markdown_list}"
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
    @mcp.tool(name="List_User", description="List Users")
    async def list_user_tool(
        context: Context,
        fields: Annotated[
            list[str] | None,
            Field(
                description="Optional list of attribute names to include as columns in the response table. When omitted, a sensible default set is used. Useful for narrowing wide entities or surfacing fields not in the default.",
                default=None,
            ),
            BeforeValidator(coerce_json),
        ],
    ) -> str:
        return await list_user(context, fields=fields)

    @mcp.tool(name="Find_User", description="Show User")
    async def find_user_tool(
        context: Context,
        id: Annotated[int | None, Field(description="User ID.", default=None)],
    ) -> str:
        return await find_user(context, id)

    @mcp.tool(name="Create_User", description="Create User")
    async def create_user_tool(
        context: Context,
        username: Annotated[
            str | None, Field(description="User's username", default=None)
        ],
        email: Annotated[
            str | None, Field(description="User's email.", default=None)
        ],
        group_ids: Annotated[
            str | None,
            Field(
                description="A list of group ids to associate this user with.  Comma delimited.",
                default=None,
            ),
        ],
        password: Annotated[
            str | None, Field(description="User password.", default=None)
        ],
        authentication_method: Annotated[
            str | None,
            Field(description="How is this user authenticated?", default=None),
        ],
        name: Annotated[
            str | None, Field(description="User's full name", default=None)
        ],
        company: Annotated[
            str | None, Field(description="User's company", default=None)
        ],
        notes: Annotated[
            str | None,
            Field(description="Any internal notes on the user", default=None),
        ],
        require_password_change: Annotated[
            bool | None,
            Field(
                description="Is a password change required upon next user login?",
                default=None,
            ),
        ],
        user_root: Annotated[
            str | None,
            Field(
                description="Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set).  Note that this is not used for API, Desktop, or Web interface.",
                default=None,
            ),
        ],
        user_home: Annotated[
            str | None,
            Field(
                description="Home folder for FTP/SFTP.  Note that this is not used for API, Desktop, or Web interface.",
                default=None,
            ),
        ],
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

    @mcp.tool(name="Update_User", description="Update User")
    async def update_user_tool(
        context: Context,
        id: Annotated[int | None, Field(description="User ID.", default=None)],
        email: Annotated[
            str | None, Field(description="User's email.", default=None)
        ],
        group_ids: Annotated[
            str | None,
            Field(
                description="A list of group ids to associate this user with.  Comma delimited.",
                default=None,
            ),
        ],
        password: Annotated[
            str | None, Field(description="User password.", default=None)
        ],
        authentication_method: Annotated[
            str | None,
            Field(description="How is this user authenticated?", default=None),
        ],
        name: Annotated[
            str | None, Field(description="User's full name", default=None)
        ],
        company: Annotated[
            str | None, Field(description="User's company", default=None)
        ],
        notes: Annotated[
            str | None,
            Field(description="Any internal notes on the user", default=None),
        ],
        require_password_change: Annotated[
            bool | None,
            Field(
                description="Is a password change required upon next user login?",
                default=None,
            ),
        ],
        user_root: Annotated[
            str | None,
            Field(
                description="Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set).  Note that this is not used for API, Desktop, or Web interface.",
                default=None,
            ),
        ],
        user_home: Annotated[
            str | None,
            Field(
                description="Home folder for FTP/SFTP.  Note that this is not used for API, Desktop, or Web interface.",
                default=None,
            ),
        ],
        username: Annotated[
            str | None, Field(description="User's username", default=None)
        ],
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

    @mcp.tool(name="Delete_User", description="Delete User")
    async def delete_user_tool(
        context: Context,
        id: Annotated[int | None, Field(description="User ID.", default=None)],
    ) -> str:
        return await delete_user(context, id)
