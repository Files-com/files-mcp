import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse

from fastmcp import Client, FastMCP
from mcp.types import TextContent
from requests import Response

from files_com_mcp.authored_tools import local_transfer
from files_com_mcp.server import create_mcp


class TestLocalTransfers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name).resolve()
        self.root = self.directory / "allowed"
        self.root.mkdir()
        self.outside = self.directory / "allowed-other"
        self.outside.mkdir()
        self.environment = patch.dict(
            os.environ, {"FILES_COM_LOCAL_ROOT": str(self.root)}
        )
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.uploaded = []

    def server(self):
        mcp = FastMCP("local-transfer-test")
        local_transfer.register_tools(mcp)
        return mcp

    def respond(self, request, **kwargs):
        response = Response()
        response.status_code = 200
        response.request = request
        response.headers["Content-Type"] = "application/json"
        path = urlparse(request.url).path
        if request.url == "https://transfer.example.test/download":
            response.raw = io.BytesIO(b"downloaded content")
        elif request.url == "https://transfer.example.test/upload":
            self.uploaded.append(request.body)
            response.headers["ETag"] = "uploaded-etag"
            response._content = b""
        elif path.startswith("/api/rest/v1/file_actions/begin_upload/"):
            response._content = json.dumps(
                [
                    {
                        "ref": "upload-ref",
                        "part_number": 1,
                        "partsize": 1024,
                        "http_method": "PUT",
                        "upload_uri": "https://transfer.example.test/upload",
                    }
                ]
            ).encode()
        elif path.startswith("/api/rest/v1/files/"):
            response._content = json.dumps(
                {"download_uri": "https://transfer.example.test/download"}
            ).encode()
        else:
            raise AssertionError(f"Unexpected request: {request.url}")
        return response

    async def transfer(self, tool, path):
        with (
            patch("files_sdk.get_api_key", return_value="testapikey"),
            patch("requests.Session.send", side_effect=self.respond) as send,
        ):
            async with Client(self.server()) as client:
                result = await client.call_tool(
                    tool,
                    {"local_path": str(path), "remote_path": "remote.txt"},
                )
        content = result.content[0]
        assert isinstance(content, TextContent)
        return content.text, send.call_count

    async def assert_transfer_round_trip(self, path):
        path.write_bytes(b"upload content")
        message, _ = await self.transfer("Upload_File_from_Local", path)
        self.assertIn("File uploaded successfully", message)
        self.assertEqual(self.uploaded.pop(), b"upload content")
        path.unlink()
        message, _ = await self.transfer("Download_File_to_Local", path)
        self.assertIn("File downloaded successfully", message)
        self.assertEqual(path.read_bytes(), b"downloaded content")

    async def test_transfers_inside_root_and_children(self):
        child = self.root / "child"
        child.mkdir()
        for directory in (self.root, child):
            with self.subTest(directory=directory):
                await self.assert_transfer_round_trip(directory / "file.txt")

    async def test_unset_or_empty_root_allows_other_directories(self):
        for value in (None, ""):
            with self.subTest(value=value):
                if value is None:
                    os.environ.pop("FILES_COM_LOCAL_ROOT", None)
                else:
                    os.environ["FILES_COM_LOCAL_ROOT"] = value
                await self.assert_transfer_round_trip(
                    self.outside / "file.txt"
                )

    async def test_relative_paths_must_resolve_inside_root(self):
        inside = Path(os.path.relpath(self.root / "file.txt"))
        await self.assert_transfer_round_trip(inside)
        outside = self.outside / "file.txt"
        outside.write_bytes(b"untouched")
        for tool in ("Upload_File_from_Local", "Download_File_to_Local"):
            message, calls = await self.transfer(
                tool, os.path.relpath(outside)
            )
            self.assertIn("Local Path Error:", message)
            self.assertEqual(calls, 0)
            self.assertEqual(outside.read_bytes(), b"untouched")

    async def test_outside_paths_are_rejected_before_transfer(self):
        outside_file = self.outside / "file.txt"
        outside_file.write_bytes(b"untouched")
        new_file = self.outside / "new.txt"
        directory_link = self.root / "directory-link"
        directory_link.symlink_to(self.outside, target_is_directory=True)
        file_link = self.root / "file-link"
        file_link.symlink_to(outside_file)
        dangling_link = self.root / "dangling-link"
        dangling_link.symlink_to(new_file)
        paths = (
            outside_file,
            self.root / ".." / "allowed-other" / "file.txt",
            directory_link / "file.txt",
            directory_link / "new.txt",
            file_link,
            dangling_link,
        )
        for tool in ("Upload_File_from_Local", "Download_File_to_Local"):
            for path in paths:
                with self.subTest(tool=tool, path=path):
                    message, calls = await self.transfer(tool, path)
                    self.assertIn("Local Path Error:", message)
                    self.assertEqual(calls, 0)
                    self.assertEqual(outside_file.read_bytes(), b"untouched")
                    self.assertFalse(new_file.exists())

    async def test_symlinks_within_root_are_allowed(self):
        target = self.root / "target.txt"
        target.write_bytes(b"upload content")
        link = self.root / "link.txt"
        link.symlink_to(target)
        message, _ = await self.transfer("Upload_File_from_Local", link)
        self.assertIn("File uploaded successfully", message)
        self.assertEqual(self.uploaded, [b"upload content"])
        message, _ = await self.transfer("Download_File_to_Local", link)
        self.assertIn("File downloaded successfully", message)
        self.assertTrue(link.is_symlink())
        self.assertEqual(target.read_bytes(), b"downloaded content")

    async def test_distinct_windows_equivalent_directories_are_rejected(self):
        allowed = self.directory / "K"
        sibling = self.directory / "\N{KELVIN SIGN}"
        allowed.mkdir()
        try:
            sibling.mkdir()
        except FileExistsError:
            self.skipTest("Filesystem treats these directory names as equal")

        os.environ["FILES_COM_LOCAL_ROOT"] = str(allowed)
        outside_file = sibling / "file.txt"
        outside_file.write_bytes(b"untouched")
        new_file = sibling / "new.txt"
        for tool in ("Upload_File_from_Local", "Download_File_to_Local"):
            for path in (outside_file, new_file):
                with self.subTest(tool=tool, path=path):
                    message, calls = await self.transfer(tool, path)
                    self.assertIn("Local Path Error:", message)
                    self.assertEqual(calls, 0)
                    self.assertEqual(outside_file.read_bytes(), b"untouched")
                    self.assertFalse(new_file.exists())

    async def test_configured_root_can_be_a_symlink(self):
        alias = self.directory / "root-link"
        alias.symlink_to(self.root, target_is_directory=True)
        os.environ["FILES_COM_LOCAL_ROOT"] = str(alias)
        await self.assert_transfer_round_trip(alias / "file.txt")

    def test_invalid_root_prevents_startup(self):
        file = self.directory / "file.txt"
        file.touch()
        for value in (
            "relative/path",
            str(file),
            str(self.directory / "missing"),
        ):
            with self.subTest(value=value):
                os.environ["FILES_COM_LOCAL_ROOT"] = value
                with self.assertRaisesRegex(
                    ValueError, "FILES_COM_LOCAL_ROOT"
                ):
                    create_mcp()


if __name__ == "__main__":
    unittest.main()
