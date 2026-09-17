import json
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlparse

from fastmcp import Client, FastMCP
from mcp.types import TextContent
from requests import Response

from files_com_mcp.generated_tools import (
    bundle,
    bundle_notification,
    bundle_recipient,
    folder,
    user,
)


class TestCreationParameters(unittest.IsolatedAsyncioTestCase):
    async def create(self, module, tool_name, arguments, path):
        mcp = FastMCP("creation-parameters-test")
        module.register_tools(mcp)
        response = Response()
        response.status_code = 200
        response._content = b'{"id": 123}'

        with (
            patch("files_sdk.get_api_key", return_value="testapikey"),
            patch("requests.Session.send", return_value=response) as send,
        ):
            async with Client(mcp) as client:
                result = await client.call_tool(tool_name, arguments)

        self.assertFalse(result.is_error)
        content = result.content[0]
        assert isinstance(content, TextContent)
        self.assertIn(" Response:\n", content.text)
        send.assert_called_once()
        request = send.call_args.args[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            unquote(urlparse(request.url).path), "/api/rest/v1" + path
        )
        return json.loads(request.body)

    async def test_creation_only_sends_supplied_settings(self):
        cases = (
            (
                user,
                "Create_User",
                {"username": "testuser"},
                {
                    "dav_permission": False,
                    "ftp_permission": False,
                    "restapi_permission": False,
                    "sftp_permission": False,
                },
                "/users",
            ),
            (
                bundle,
                "Create_Bundle",
                {"paths": ["shared"]},
                {"permissions": "write"},
                "/bundles",
            ),
            (
                bundle_recipient,
                "Create_Bundle_Recipient",
                {"bundle_id": 123, "recipient": "recipient@example.test"},
                {"share_after_create": False},
                "/bundle_recipients",
            ),
            (
                bundle_notification,
                "Create_Bundle_Notification",
                {"bundle_id": 123},
                {"notify_on_registration": False, "notify_on_upload": True},
                "/bundle_notifications",
            ),
        )
        for module, tool_name, required, settings, path in cases:
            for arguments in (required, required | settings):
                with self.subTest(tool=tool_name, arguments=arguments):
                    params = await self.create(
                        module, tool_name, arguments, path
                    )
                    self.assertEqual(params, arguments)

    async def test_nested_folder_creation_requests_missing_parents(self):
        params = await self.create(
            folder,
            "Create_Folder",
            {"path": "parent/child"},
            "/folders/parent/child",
        )
        self.assertEqual(
            params, {"path": "parent/child", "mkdir_parents": True}
        )


if __name__ == "__main__":
    unittest.main()
