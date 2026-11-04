import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastmcp import Client
from mcp.types import TextContent

import files_sdk
import files_sdk.error
from files_com_mcp.server import create_mcp
from tests.loopback_api import serve_loopback_api


class ToolCallTest(unittest.IsolatedAsyncioTestCase):
    api_key: str | None = "mcptestkey"

    def setUp(self):
        self.api = serve_loopback_api(self, self.api_key)

    async def call(self, tool, arguments):
        async with Client(create_mcp()) as client:
            result = await client.call_tool(
                tool, arguments, raise_on_error=False
            )
        [content] = result.content
        assert isinstance(content, TextContent)
        self.assertNotIn(self.api_key or "no key", content.text)
        return result.is_error, content.text


class TestToolErrors(ToolCallTest):
    """Failed tool calls reach clients as tool results with isError set,
    and a successful call, however empty, does not."""

    async def test_api_errors_are_tool_errors(self):
        for status, error_type, message in (
            (
                403,
                "not-authorized/insufficient-permission-for-params",
                "You do not have permission",
            ),
            (404, "not-found/user-not-found", "User Not Found"),
            (422, "processing-failure/invalid-input", "Invalid input"),
        ):
            with self.subTest(status=status):
                self.api.reply_json(
                    {
                        "type": error_type,
                        "http-code": status,
                        "error": message,
                    },
                    status=status,
                )
                error, text = await self.call("Find_User", {"id": 99})
                self.assertTrue(error)
                self.assertTrue(text.startswith("Files.com Error:"), text)
                self.assertIn(message, text)

    async def test_rejected_api_key_is_an_authentication_error(self):
        self.api.reply_json(
            {
                "type": "not-authenticated/authentication-required",
                "http-code": 401,
                "error": "Authentication required",
            },
            status=401,
        )
        error, text = await self.call("Find_User", {"id": 99})
        self.assertTrue(error)
        self.assertTrue(text.startswith("Authentication Error:"), text)
        self.assertIn("Authentication required", text)

    async def test_missing_required_input_is_rejected_before_any_request(self):
        error, text = await self.call("Create_User", {"name": "No Username"})
        self.assertTrue(error)
        self.assertEqual(text, "Missing required parameter: username")
        self.assertEqual(self.api.requests, [])

    async def test_malformed_input_is_rejected_before_any_request(self):
        error, text = await self.call("Find_User", {"id": "not a number"})
        self.assertTrue(error)
        self.assertIn("id", text)
        self.assertEqual(self.api.requests, [])

    async def test_request_that_times_out_is_a_tool_error(self):
        self.api.hold_json({"id": 1})
        with patch.object(files_sdk, "read_timeout", 0.5):
            error, text = await self.call("Find_User", {"id": 1})
        self.assertTrue(error)
        self.assertTrue(text.startswith("Files.com Error:"), text)
        self.assertEqual(len(self.api.requests), 1)

    async def test_object_arguments_reach_the_request(self):
        # Some clients send object arguments as JSON text.
        for value in ({"username": "pat"}, '{"username": "pat"}'):
            with self.subTest(value=value):
                self.api.requests.clear()
                self.api.reply_json([])
                error, text = await self.call(
                    "List_Sftp_Action_Log", {"filter": value}
                )
                self.assertEqual(
                    (error, text), (False, "No sftpactionlogs found.")
                )
                [request] = self.api.requests
                self.assertEqual(request.query, {"filter[username]": "pat"})

    async def test_empty_list_is_a_successful_result(self):
        self.api.reply_json([])
        error, text = await self.call("List_User", {})
        self.assertFalse(error)
        self.assertEqual(text, "No users found.")

    async def test_failed_upload_is_a_tool_error(self):
        with tempfile.TemporaryDirectory() as directory:
            local = Path(directory) / "upload.bin"
            local.write_bytes(b"upload bytes")
            self.api.reply_json(
                [
                    {
                        "ref": "upload-ref",
                        "part_number": 1,
                        "partsize": 1024,
                        "http_method": "PUT",
                        "upload_uri": self.api.url + "/storage/part-1",
                    }
                ]
            )
            self.api.reply(500, b"storage unavailable")
            error, text = await self.call(
                "Upload_File_from_Local",
                {"local_path": str(local), "remote_path": "remote.bin"},
            )
        self.assertTrue(error)
        self.assertNotIn("successfully", text)
        # Nothing asked Files.com to complete the failed upload.
        self.assertEqual(
            [request.url_path for request in self.api.requests],
            [
                "/api/rest/v1/file_actions/begin_upload/remote.bin",
                "/storage/part-1",
            ],
        )

    async def test_failed_download_shows_storage_explanation_only(self):
        # The SDK adds file storage's explanation of a failed download to the
        # error it raises, as a note beside the download_request_status it
        # read, a files_sdk.DownloadRequestStatus (files_sdk.download). A note
        # on any other error, such as a cleanup failure, is the SDK's
        # diagnostic, not the tool's result.
        explanation = (
            "File storage's status of this download request: Upstream "
            "refused (status failed, 3 bytes transferred)"
        )
        explained = files_sdk.error.APIError(
            "Transfer request failed", http_status=422
        )
        explained.download_request_status = files_sdk.DownloadRequestStatus(
            status="failed", bytes_transferred=3, error="Upstream refused"
        )
        explained.add_note(explanation)
        other = files_sdk.error.APIError(
            "Transfer request failed", http_status=422
        )
        other.add_note("Closing an attachment afterwards also failed")
        failed = "Files.com Error: HTTP 422 Transfer request failed"
        with tempfile.TemporaryDirectory() as directory:
            arguments = {
                "remote_path": "remote.bin",
                "local_path": str(Path(directory) / "download.bin"),
            }
            for failure, expected in (
                (explained, f"{failed}\n{explanation}"),
                (other, failed),
            ):
                with (
                    self.subTest(expected=expected),
                    patch("files_sdk.file.download_file", side_effect=failure),
                ):
                    error, text = await self.call(
                        "Download_File_to_Local", arguments
                    )
                self.assertTrue(error)
                self.assertEqual(text, expected)


class TestMissingApiKey(ToolCallTest):
    api_key = None

    async def test_calls_fail_with_setup_instructions(self):
        error, text = await self.call("Find_User", {"id": 99})
        self.assertTrue(error)
        self.assertTrue(text.startswith("Authentication Error:"), text)
        self.assertIn("FILES_COM_API_KEY", text)
        self.assertEqual(self.api.requests, [])


if __name__ == "__main__":
    unittest.main()
