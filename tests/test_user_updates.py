import json
import unittest
from unittest.mock import patch
from urllib.parse import urlparse

from fastmcp import Client, FastMCP
from mcp.types import TextContent
from requests import Response

from files_com_mcp.generated_tools import user


class TestUserUpdates(unittest.IsolatedAsyncioTestCase):
    async def update_user(self, arguments):
        mcp = FastMCP("user-update-test")
        user.register_tools(mcp)
        response = Response()
        response.status_code = 200
        response._content = json.dumps(
            {"id": 123, "notes": "Updated notes"}
        ).encode()

        with (
            patch("files_sdk.get_api_key", return_value="testapikey"),
            patch("requests.Session.send", return_value=response) as send,
        ):
            async with Client(mcp) as client:
                result = await client.call_tool("Update_User", arguments)

        self.assertFalse(result.is_error)
        content = result.content[0]
        assert isinstance(content, TextContent)
        self.assertIn("User Response:\n", content.text)
        send.assert_called_once()
        request = send.call_args.args[0]
        self.assertEqual(request.method, "PATCH")
        self.assertEqual(urlparse(request.url).path, "/api/rest/v1/users/123")
        return json.loads(request.body)

    async def test_notes_only_update_does_not_send_protocol_permissions(self):
        params = await self.update_user({"id": 123, "notes": "Updated notes"})
        self.assertEqual(params, {"id": 123, "notes": "Updated notes"})

    async def test_update_sends_only_explicit_protocol_permissions(self):
        for permission in (
            "dav_permission",
            "ftp_permission",
            "restapi_permission",
            "sftp_permission",
        ):
            for value in (False, True):
                with self.subTest(permission=permission, value=value):
                    arguments = {"id": 123, permission: value}
                    self.assertEqual(
                        await self.update_user(arguments), arguments
                    )


if __name__ == "__main__":
    unittest.main()
