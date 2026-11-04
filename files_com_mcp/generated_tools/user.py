from fastmcp import Context
from fastmcp.exceptions import ToolError
from typing_extensions import Annotated
from pydantic import BeforeValidator, Field
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.utils import coerce_json, object_list_to_markdown_table
import files_sdk


async def list_user(
    context: Context,
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
    """List Users

    Args:
        cursor: Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page: Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """

    params = {}
    if cursor is not None:
        params["cursor"] = cursor
    if per_page is not None:
        params["per_page"] = per_page

    def call(options):
        # One page; the response tells the caller how to fetch the next.
        page = files_sdk.user.list(params, options)
        return list(page), page.cursor

    retval, next_cursor = await call_files_api(context, call)
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
            "ai_assistant_personality_id",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
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
            "notify_on_all_site_warnings",
            "notify_on_all_sso_failures",
            "notify_on_all_user_security_events",
            "notify_on_all_pending_work_failures",
            "notify_on_all_siem_http_destination_failures",
            "notify_on_all_sync_failures",
            "notify_on_all_automation_failures",
            "notify_on_all_expectation_failures",
            "require_2fa",
            "require_login_by",
            "active_2fa",
            "require_password_change",
            "password_expired",
            "responsible_group_id",
            "responsible_user_id",
            "readonly_site_admin",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "self_managed",
            "sftp_permission",
            "site_admin",
            "workspace_admin",
            "site_id",
            "workspace_id",
            "default_workspace_id",
            "skip_welcome_screen",
            "ftp_tls_session_reuse_required",
            "ssl_required",
            "sso_strategy_id",
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


async def find_user(
    context: Context,
    id: Annotated[int | None, Field(description="User ID.", default=None)],
) -> str:
    """Show User

    Args:
        id: User ID.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        return [files_sdk.user.find(id, params, options)], None

    retval, next_cursor = await call_files_api(context, call)

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
            "ai_assistant_personality_id",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
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
            "notify_on_all_site_warnings",
            "notify_on_all_sso_failures",
            "notify_on_all_user_security_events",
            "notify_on_all_pending_work_failures",
            "notify_on_all_siem_http_destination_failures",
            "notify_on_all_sync_failures",
            "notify_on_all_automation_failures",
            "notify_on_all_expectation_failures",
            "require_2fa",
            "require_login_by",
            "active_2fa",
            "require_password_change",
            "password_expired",
            "responsible_group_id",
            "responsible_user_id",
            "readonly_site_admin",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "self_managed",
            "sftp_permission",
            "site_admin",
            "workspace_admin",
            "site_id",
            "workspace_id",
            "default_workspace_id",
            "skip_welcome_screen",
            "ftp_tls_session_reuse_required",
            "ssl_required",
            "sso_strategy_id",
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
    dav_permission: Annotated[
        bool | None,
        Field(description="Can the user connect with WebDAV?", default=None),
    ],
    ftp_permission: Annotated[
        bool | None,
        Field(description="Can the user access with FTP/FTPS?", default=None),
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
    restapi_permission: Annotated[
        bool | None,
        Field(
            description="Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)",
            default=None,
        ),
    ],
    s3_compatible_endpoint_permission: Annotated[
        bool | None,
        Field(
            description="Can the user access the S3-compatible endpoint? Defaults to true.",
            default=None,
        ),
    ],
    sftp_permission: Annotated[
        bool | None,
        Field(description="Can the user access with SFTP?", default=None),
    ],
    user_root: Annotated[
        str | None,
        Field(
            description="If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.",
            default=None,
        ),
    ],
    user_home: Annotated[
        str | None,
        Field(
            description="Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.",
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
        dav_permission: Can the user connect with WebDAV?
        ftp_permission: Can the user access with FTP/FTPS?
        name: User's full name
        company: User's company
        notes: Any internal notes on the user
        require_password_change: Is a password change required upon next user login?
        restapi_permission: Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
        s3_compatible_endpoint_permission: Can the user access the S3-compatible endpoint? Defaults to true.
        sftp_permission: Can the user access with SFTP?
        user_root: If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
        user_home: Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
    """

    params = {}
    if username is None:
        raise ToolError("Missing required parameter: username")
    params["username"] = username
    if email is not None:
        params["email"] = email
    if group_ids is not None:
        params["group_ids"] = group_ids
    if password is not None:
        params["password"] = password
    if authentication_method is not None:
        params["authentication_method"] = authentication_method
    if dav_permission is not None:
        params["dav_permission"] = dav_permission
    if ftp_permission is not None:
        params["ftp_permission"] = ftp_permission
    if name is not None:
        params["name"] = name
    if company is not None:
        params["company"] = company
    if notes is not None:
        params["notes"] = notes
    if require_password_change is not None:
        params["require_password_change"] = require_password_change
    if restapi_permission is not None:
        params["restapi_permission"] = restapi_permission
    if s3_compatible_endpoint_permission is not None:
        params["s3_compatible_endpoint_permission"] = (
            s3_compatible_endpoint_permission
        )
    if sftp_permission is not None:
        params["sftp_permission"] = sftp_permission
    if user_root is not None:
        params["user_root"] = user_root
    if user_home is not None:
        params["user_home"] = user_home

    def call(options):
        return [files_sdk.user.create(params, options)], None

    retval, next_cursor = await call_files_api(context, call)

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
            "ai_assistant_personality_id",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
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
            "notify_on_all_site_warnings",
            "notify_on_all_sso_failures",
            "notify_on_all_user_security_events",
            "notify_on_all_pending_work_failures",
            "notify_on_all_siem_http_destination_failures",
            "notify_on_all_sync_failures",
            "notify_on_all_automation_failures",
            "notify_on_all_expectation_failures",
            "require_2fa",
            "require_login_by",
            "active_2fa",
            "require_password_change",
            "password_expired",
            "responsible_group_id",
            "responsible_user_id",
            "readonly_site_admin",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "self_managed",
            "sftp_permission",
            "site_admin",
            "workspace_admin",
            "site_id",
            "workspace_id",
            "default_workspace_id",
            "skip_welcome_screen",
            "ftp_tls_session_reuse_required",
            "ssl_required",
            "sso_strategy_id",
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
    dav_permission: Annotated[
        bool | None,
        Field(description="Can the user connect with WebDAV?", default=None),
    ],
    ftp_permission: Annotated[
        bool | None,
        Field(description="Can the user access with FTP/FTPS?", default=None),
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
    restapi_permission: Annotated[
        bool | None,
        Field(
            description="Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)",
            default=None,
        ),
    ],
    s3_compatible_endpoint_permission: Annotated[
        bool | None,
        Field(
            description="Can the user access the S3-compatible endpoint? Defaults to true.",
            default=None,
        ),
    ],
    sftp_permission: Annotated[
        bool | None,
        Field(description="Can the user access with SFTP?", default=None),
    ],
    user_root: Annotated[
        str | None,
        Field(
            description="If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.",
            default=None,
        ),
    ],
    user_home: Annotated[
        str | None,
        Field(
            description="Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.",
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
        dav_permission: Can the user connect with WebDAV?
        ftp_permission: Can the user access with FTP/FTPS?
        name: User's full name
        company: User's company
        notes: Any internal notes on the user
        require_password_change: Is a password change required upon next user login?
        restapi_permission: Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
        s3_compatible_endpoint_permission: Can the user access the S3-compatible endpoint? Defaults to true.
        sftp_permission: Can the user access with SFTP?
        user_root: If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
        user_home: Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
        username: User's username
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id
    if email is not None:
        params["email"] = email
    if group_ids is not None:
        params["group_ids"] = group_ids
    if password is not None:
        params["password"] = password
    if authentication_method is not None:
        params["authentication_method"] = authentication_method
    if dav_permission is not None:
        params["dav_permission"] = dav_permission
    if ftp_permission is not None:
        params["ftp_permission"] = ftp_permission
    if name is not None:
        params["name"] = name
    if company is not None:
        params["company"] = company
    if notes is not None:
        params["notes"] = notes
    if require_password_change is not None:
        params["require_password_change"] = require_password_change
    if restapi_permission is not None:
        params["restapi_permission"] = restapi_permission
    if s3_compatible_endpoint_permission is not None:
        params["s3_compatible_endpoint_permission"] = (
            s3_compatible_endpoint_permission
        )
    if sftp_permission is not None:
        params["sftp_permission"] = sftp_permission
    if user_root is not None:
        params["user_root"] = user_root
    if user_home is not None:
        params["user_home"] = user_home
    if username is not None:
        params["username"] = username

    def call(options):
        return [files_sdk.user.update(id, params, options)], None

    retval, next_cursor = await call_files_api(context, call)

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
            "ai_assistant_personality_id",
            "desktop_configuration_profile_id",
            "integration_centric_profile_id",
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
            "notify_on_all_site_warnings",
            "notify_on_all_sso_failures",
            "notify_on_all_user_security_events",
            "notify_on_all_pending_work_failures",
            "notify_on_all_siem_http_destination_failures",
            "notify_on_all_sync_failures",
            "notify_on_all_automation_failures",
            "notify_on_all_expectation_failures",
            "require_2fa",
            "require_login_by",
            "active_2fa",
            "require_password_change",
            "password_expired",
            "responsible_group_id",
            "responsible_user_id",
            "readonly_site_admin",
            "restapi_permission",
            "s3_compatible_endpoint_permission",
            "self_managed",
            "sftp_permission",
            "site_admin",
            "workspace_admin",
            "site_id",
            "workspace_id",
            "default_workspace_id",
            "skip_welcome_screen",
            "ftp_tls_session_reuse_required",
            "ssl_required",
            "sso_strategy_id",
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


async def delete_user(
    context: Context,
    id: Annotated[int | None, Field(description="User ID.", default=None)],
) -> str:
    """Delete User

    Args:
        id: User ID.
    """

    params = {}
    if id is None:
        raise ToolError("Missing required parameter: id")
    params["id"] = id

    def call(options):
        # The API returns no record for this operation.
        files_sdk.user.delete(id, params, options)
        return [], None

    retval, next_cursor = await call_files_api(context, call)

    markdown_list = object_list_to_markdown_table(retval, [])
    response = f"User Response:\n{markdown_list}"
    if next_cursor:
        response += f"\n\nMore results available. Pass cursor={next_cursor!r} to fetch the next page."
    return response


def register_tools(mcp):
    @mcp.tool(
        name="List_User",
        description="List Users",
        annotations={
            "title": "List User",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def list_user_tool(
        context: Context,
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
        return await list_user(context, cursor, per_page, fields=fields)

    @mcp.tool(
        name="Find_User",
        description="Show User",
        annotations={
            "title": "Find User",
            "openWorldHint": False,
            "readOnlyHint": True,
        },
    )
    async def find_user_tool(
        context: Context,
        id: Annotated[int | None, Field(description="User ID.", default=None)],
    ) -> str:
        return await find_user(context, id)

    @mcp.tool(
        name="Create_User",
        description="Create User",
        annotations={
            "title": "Create User",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": False,
        },
    )
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
        dav_permission: Annotated[
            bool | None,
            Field(
                description="Can the user connect with WebDAV?", default=None
            ),
        ],
        ftp_permission: Annotated[
            bool | None,
            Field(
                description="Can the user access with FTP/FTPS?", default=None
            ),
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
        restapi_permission: Annotated[
            bool | None,
            Field(
                description="Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)",
                default=None,
            ),
        ],
        s3_compatible_endpoint_permission: Annotated[
            bool | None,
            Field(
                description="Can the user access the S3-compatible endpoint? Defaults to true.",
                default=None,
            ),
        ],
        sftp_permission: Annotated[
            bool | None,
            Field(description="Can the user access with SFTP?", default=None),
        ],
        user_root: Annotated[
            str | None,
            Field(
                description="If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.",
                default=None,
            ),
        ],
        user_home: Annotated[
            str | None,
            Field(
                description="Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.",
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
            dav_permission,
            ftp_permission,
            name,
            company,
            notes,
            require_password_change,
            restapi_permission,
            s3_compatible_endpoint_permission,
            sftp_permission,
            user_root,
            user_home,
        )

    @mcp.tool(
        name="Update_User",
        description="Update User",
        annotations={
            "title": "Update User",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": True,
        },
    )
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
        dav_permission: Annotated[
            bool | None,
            Field(
                description="Can the user connect with WebDAV?", default=None
            ),
        ],
        ftp_permission: Annotated[
            bool | None,
            Field(
                description="Can the user access with FTP/FTPS?", default=None
            ),
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
        restapi_permission: Annotated[
            bool | None,
            Field(
                description="Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)",
                default=None,
            ),
        ],
        s3_compatible_endpoint_permission: Annotated[
            bool | None,
            Field(
                description="Can the user access the S3-compatible endpoint? Defaults to true.",
                default=None,
            ),
        ],
        sftp_permission: Annotated[
            bool | None,
            Field(description="Can the user access with SFTP?", default=None),
        ],
        user_root: Annotated[
            str | None,
            Field(
                description="If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.",
                default=None,
            ),
        ],
        user_home: Annotated[
            str | None,
            Field(
                description="Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.",
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
            dav_permission,
            ftp_permission,
            name,
            company,
            notes,
            require_password_change,
            restapi_permission,
            s3_compatible_endpoint_permission,
            sftp_permission,
            user_root,
            user_home,
            username,
        )

    @mcp.tool(
        name="Delete_User",
        description="Delete User",
        annotations={
            "title": "Delete User",
            "openWorldHint": False,
            "readOnlyHint": False,
            "destructiveHint": True,
        },
    )
    async def delete_user_tool(
        context: Context,
        id: Annotated[int | None, Field(description="User ID.", default=None)],
    ) -> str:
        return await delete_user(context, id)
