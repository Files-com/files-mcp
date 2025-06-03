from fastmcp import Context
from files_com_mcp.utils import object_list_to_markdown_table
import files_sdk
import files_sdk.error


async def list_automation(context: Context) -> str:
    """List Automations"""

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}

        retval = files_sdk.automation.list(params, options)
        retval = [item for item in retval.auto_paging_iter()]
        if not retval:
            return "No automations found."

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "always_overwrite_size_matching_files",
                "automation",
                "deleted",
                "description",
                "destination_replace_from",
                "destination_replace_to",
                "destinations",
                "disabled",
                "exclude_pattern",
                "import_urls",
                "flatten_destination_structure",
                "group_ids",
                "ignore_locked_folders",
                "interval",
                "last_modified_at",
                "legacy_folder_matching",
                "name",
                "overwrite_files",
                "path",
                "path_time_zone",
                "recurring_day",
                "retry_on_failure_interval_in_minutes",
                "retry_on_failure_number_of_attempts",
                "schedule",
                "human_readable_schedule",
                "schedule_days_of_week",
                "schedule_times_of_day",
                "schedule_time_zone",
                "source",
                "sync_ids",
                "trigger_actions",
                "trigger",
                "user_id",
                "user_ids",
                "value",
                "webhook_url",
            ],
        )
        return f"Automation Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


async def find_automation(context: Context, id: int | None = None) -> str:
    """Show Automation

    Args:
        id: Automation ID.
    """

    try:
        options = {
            "api_key": context.request_context.session._files_com_api_key
        }
        params = {}
        if id is None:
            return "Missing required parameter: id"
        params["id"] = id

        retval = files_sdk.automation.find(id, params, options)
        retval = [retval]

        markdown_list = object_list_to_markdown_table(
            retval,
            [
                "id",
                "always_overwrite_size_matching_files",
                "automation",
                "deleted",
                "description",
                "destination_replace_from",
                "destination_replace_to",
                "destinations",
                "disabled",
                "exclude_pattern",
                "import_urls",
                "flatten_destination_structure",
                "group_ids",
                "ignore_locked_folders",
                "interval",
                "last_modified_at",
                "legacy_folder_matching",
                "name",
                "overwrite_files",
                "path",
                "path_time_zone",
                "recurring_day",
                "retry_on_failure_interval_in_minutes",
                "retry_on_failure_number_of_attempts",
                "schedule",
                "human_readable_schedule",
                "schedule_days_of_week",
                "schedule_times_of_day",
                "schedule_time_zone",
                "source",
                "sync_ids",
                "trigger_actions",
                "trigger",
                "user_id",
                "user_ids",
                "value",
                "webhook_url",
            ],
        )
        return f"Automation Response:\n{markdown_list}"
    except files_sdk.error.NotAuthenticatedError as err:
        return f"Authentication Error: {err}"
    except files_sdk.error.Error as err:
        return f"Files.com Error: {err}"
    except Exception as ex:
        return f"General Exception: {ex}"


def register_tools(mcp):
    @mcp.tool(name="List_Automation")
    async def list_automation_tool(context: Context) -> str:
        return await list_automation(context)

    @mcp.tool(name="Find_Automation")
    async def find_automation_tool(
        context: Context, id: int | None = None
    ) -> str:
        return await find_automation(context, id)
