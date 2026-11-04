import contextlib
import json
import os
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

from tests import stdio_server
from tests.loopback_api import start_loopback_api

API_KEY = "mcpstdiocanarykey"
PROTOCOL_VERSION = "2025-11-25"
AUTHORED_TOOLS = {"Download_File_to_Local", "Upload_File_from_Local"}
GENERATED_TOOLS = json.loads(
    (Path(__file__).parent / "generated_tools.json").read_text()
)
SIGNATURE = "?X-Amz-Signature=signed"


class TestStdio(unittest.IsolatedAsyncioTestCase):
    """The server as an MCP client runs it, against a stand-in Files.com
    API: a child process started with the API key in its environment and
    driven over STDIO with the official MCP client."""

    def setUp(self):
        self.api = start_loopback_api(self)
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name).resolve()
        self.root = self.scratch / "local files"
        self.root.mkdir()
        self.stderr = self.scratch / "stderr.log"

    @contextlib.asynccontextmanager
    async def connect(self, command=None, api_key: str | None = API_KEY):
        command = command or stdio_server.module_command()
        server = StdioServerParameters(
            command=command[0],
            args=command[1:],
            env=stdio_server.environment(
                FILES_COM_API_KEY=api_key,
                FILES_COM_BASE_URL=self.api.url,
                FILES_COM_LOCAL_ROOT=str(self.root),
            ),
            cwd=stdio_server.working_directory(self.scratch),
        )
        with open(self.stderr, "a") as errlog:
            async with stdio_client(server, errlog=errlog) as streams:
                async with ClientSession(
                    *streams, read_timeout_seconds=timedelta(seconds=20)
                ) as session:
                    self.initialized = await session.initialize()
                    yield session
        # Diagnostics go to stderr, never the API key.
        self.assertNotIn(API_KEY, self.stderr.read_text())

    async def call(self, session, tool, arguments=None):
        result = await session.call_tool(tool, arguments or {})
        [content] = result.content
        assert isinstance(content, TextContent)
        self.assertNotIn(API_KEY, content.text)
        return result.isError, content.text

    def api_requests(self):
        return [r for r in self.api.requests if r.url_path.startswith("/api/")]

    async def test_lists_exactly_the_generated_and_local_transfer_tools(self):
        async with self.connect() as session:
            tools = (await session.list_tools()).tools
        self.assertEqual(self.initialized.protocolVersion, PROTOCOL_VERSION)
        self.assertEqual(self.initialized.serverInfo.name, "filescom")

        listed = {tool.name: tool for tool in tools}
        self.assertEqual(
            set(listed),
            {tool["name"] for tool in GENERATED_TOOLS} | AUTHORED_TOOLS,
        )
        for expected in GENERATED_TOOLS:
            with self.subTest(tool=expected["name"]):
                tool = listed[expected["name"]]
                assert tool.annotations is not None
                self.assertEqual(
                    tool.annotations.model_dump(exclude_none=True),
                    expected["annotations"],
                )
                self.assertEqual(
                    sorted(tool.inputSchema.get("properties", {})),
                    sorted(expected["parameters"]),
                )
                # The tool itself reports a missing required input.
                self.assertEqual(tool.inputSchema.get("required", []), [])
        for name in AUTHORED_TOOLS:
            self.assertEqual(
                sorted(listed[name].inputSchema["required"]),
                ["local_path", "remote_path"],
            )

    async def test_lists_one_page_at_a_time_with_the_cursor_it_returns(self):
        self.api.reply_json(
            [{"id": 1, "username": "pat"}, {"id": 2, "username": "robin"}],
            headers={"X-Files-Cursor": "cursor-for-page-2"},
        )
        self.api.reply_json([{"id": 3, "username": "sam"}])
        self.api.reply_json([])
        async with self.connect() as session:
            first = await self.call(session, "List_User", {"per_page": 2})
            last = await self.call(
                session,
                "List_User",
                {"per_page": 2, "cursor": "cursor-for-page-2"},
            )
            empty = await self.call(session, "List_User")

        error, text = first
        self.assertFalse(error)
        self.assertIn("| 1 | pat |", text)
        self.assertIn("| 2 | robin |", text)
        self.assertTrue(
            text.endswith(
                "\n\nMore results available. Pass cursor='cursor-for-page-2' "
                "to fetch the next page."
            ),
            text,
        )
        error, text = last
        self.assertFalse(error)
        self.assertIn("| 3 | sam |", text)
        self.assertNotIn("More results", text)
        self.assertEqual(empty, (False, "No users found."))

        # One request per call: no page is fetched that was not asked for.
        self.assertEqual(
            [(r.path, r.query) for r in self.api.requests],
            [
                ("/users", {"per_page": "2"}),
                ("/users", {"per_page": "2", "cursor": "cursor-for-page-2"}),
                ("/users", {}),
            ],
        )
        self.assertEqual(
            {r.headers["X-FilesAPI-Key"] for r in self.api.requests},
            {API_KEY},
        )

    async def test_renders_selected_fields_with_their_values(self):
        user = {
            "id": 0,
            "username": "zoë",
            "site_admin": False,
            "notes": None,
            "name": "Zoë | Quinn\nReviewer",
            "admin_group_ids": [1, 2],
        }
        self.api.reply_json([user])
        self.api.reply_json([user])
        fields = [
            "id",
            "username",
            "site_admin",
            "notes",
            "name",
            "admin_group_ids",
            "options",
            "__dict__",
        ]
        async with self.connect() as session:
            native = await self.call(session, "List_User", {"fields": fields})
            # Some clients send array arguments as JSON text.
            text_argument = await self.call(
                session, "List_User", {"fields": json.dumps(fields)}
            )
        expected = (
            "User Response:\n"
            "| id | username | site_admin | notes | name | admin_group_ids |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| 0 | zoë | False |  | Zoë \\| Quinn Reviewer | [1, 2] |"
        )
        self.assertEqual(native, (False, expected))
        self.assertEqual(text_argument, (False, expected))

    async def test_sends_exactly_the_values_given_and_reports_failures(self):
        self.api.reply_json({"id": 7, "username": "newuser"})
        self.api.reply_json({"id": 11})
        self.api.reply_json({"id": 12, "bundle_id": 0})
        self.api.reply_json({"id": 7, "notes": "New notes"})
        self.api.reply(204)
        self.api.reply_json(
            {"type": "not-found/user-not-found", "error": "User Not Found"},
            status=404,
        )
        self.api.reply_json(
            {
                "type": "not-authorized/insufficient-permission-for-params",
                "error": "Not allowed",
            },
            status=403,
        )
        async with self.connect() as session:
            results = [
                await self.call(session, tool, arguments)
                for tool, arguments in (
                    (
                        "Create_User",
                        {
                            "username": "newuser",
                            "dav_permission": False,
                            "ftp_permission": True,
                        },
                    ),
                    # Some clients send array arguments as JSON text.
                    ("Create_Bundle", {"paths": '["shared", "reports"]'}),
                    ("Create_Bundle_Notification", {"bundle_id": 0}),
                    ("Update_User", {"id": 7, "notes": "New notes"}),
                    ("Delete_User", {"id": 7}),
                    ("Find_User", {"id": 99}),
                    ("Find_User", {"id": 98}),
                    ("Create_User", {"email": "no-username@example.test"}),
                )
            ]

        self.assertEqual(
            [error for error, _ in results], [False] * 5 + [True] * 3
        )
        self.assertIn("newuser", results[0][1])
        self.assertTrue(results[5][1].startswith("Files.com Error:"))
        self.assertIn("User Not Found", results[5][1])
        self.assertIn("Not allowed", results[6][1])
        self.assertEqual(results[7][1], "Missing required parameter: username")
        # The notes-only update leaves every protocol permission alone; the
        # missing username stopped the last call before any request.
        self.assertEqual(
            [(r.method, r.path, r.json) for r in self.api.requests],
            [
                (
                    "POST",
                    "/users",
                    {
                        "username": "newuser",
                        "dav_permission": False,
                        "ftp_permission": True,
                    },
                ),
                ("POST", "/bundles", {"paths": ["shared", "reports"]}),
                ("POST", "/bundle_notifications", {"bundle_id": 0}),
                ("PATCH", "/users/7", {"id": 7, "notes": "New notes"}),
                ("DELETE", "/users/7", None),
                ("GET", "/users/99", None),
                ("GET", "/users/98", None),
            ],
        )

    async def test_shows_the_record_each_operation_returns(self):
        # A file action returns a FileAction, not the File it acts on; a ZIP
        # listing returns its entries; a deletion returns nothing.
        self.api.reply_json({"status": "completed"}, status=201)
        self.api.reply_json(
            {"status": "pending", "file_migration_id": 42}, status=201
        )
        self.api.reply_json(
            [
                {"path": "docs/a.txt", "size": 12},
                {"path": "docs/empty.bin", "size": 0},
            ]
        )
        self.api.reply_json([])
        self.api.reply(204)
        self.api.reply_json({"path": "docs", "type": "directory"}, status=201)
        async with self.connect() as session:
            copied = await self.call(
                session, "Copy_File", {"path": "a.txt", "destination": "b.txt"}
            )
            moved = await self.call(
                session, "Move_File", {"path": "big", "destination": "old/big"}
            )
            entries = await self.call(
                session, "Zip_List_Contents_File", {"path": "docs.zip"}
            )
            no_entries = await self.call(
                session, "Zip_List_Contents_File", {"path": "empty.zip"}
            )
            deleted = await self.call(session, "Delete_User", {"id": 7})
            folder = await self.call(
                session, "Create_Folder", {"path": "docs"}
            )

        self.assertEqual(
            copied,
            (
                False,
                "File Response:\n"
                "| status | file_migration_id |\n"
                "| --- | --- |\n"
                "| completed |  |",
            ),
        )
        self.assertEqual(
            moved,
            (
                False,
                "File Response:\n"
                "| status | file_migration_id |\n"
                "| --- | --- |\n"
                "| pending | 42 |",
            ),
        )
        self.assertEqual(
            entries,
            (
                False,
                "File Response:\n"
                "| path | size |\n"
                "| --- | --- |\n"
                "| docs/a.txt | 12 |\n"
                "| docs/empty.bin | 0 |",
            ),
        )
        self.assertEqual(no_entries, (False, "No files found."))
        self.assertEqual(deleted, (False, "User Response:\n*(no data)*"))
        # Creating a folder still shows the File record the API returns.
        error, text = folder
        self.assertFalse(error)
        title, header, _, row = text.split("\n")
        self.assertEqual(title, "Folder Response:")
        values = dict(zip(header[2:-2].split(" | "), row[2:-2].split(" | ")))
        self.assertEqual(values["path"], "docs")
        self.assertEqual(values["type"], "directory")
        self.assertEqual(
            [(r.method, r.path) for r in self.api.requests],
            [
                ("POST", "/file_actions/copy/a.txt"),
                ("POST", "/file_actions/move/big"),
                ("GET", "/file_actions/zip_list/docs.zip"),
                ("GET", "/file_actions/zip_list/empty.zip"),
                ("DELETE", "/users/7"),
                ("POST", "/folders/docs"),
            ],
        )

    def reply_to_upload(self, remote):
        self.api.reply_json(
            [
                {
                    "ref": "upload-ref",
                    "part_number": 1,
                    "partsize": 5242880,
                    "http_method": "PUT",
                    "upload_uri": self.api.url + "/storage/part" + SIGNATURE,
                }
            ]
        )
        self.api.reply(200, headers={"ETag": '"part-etag"'})
        self.api.reply_json({"path": remote, "type": "file"})

    def reply_to_download(self, remote, data):
        self.api.reply_json(
            {
                "path": remote,
                "type": "file",
                "size": len(data),
                "download_uri": self.api.url + "/storage/file" + SIGNATURE,
            }
        )
        self.api.reply(200, data, {"Content-Type": "application/octet-stream"})

    async def test_transfers_exact_bytes_within_the_local_root_only(self):
        every_byte = bytes(range(256)) * 3
        empty_upload = self.root / "empty upload.txt"
        empty_upload.write_bytes(b"")
        nested = self.root / "Zoë files"
        nested.mkdir()
        (nested / "every byte.bin").write_bytes(every_byte)
        outside = self.scratch / "outside.txt"
        outside.write_bytes(b"outside")
        (self.root / "escape").symlink_to(
            self.scratch, target_is_directory=True
        )
        existing = self.root / "existing.bin"
        existing.write_bytes(b"old contents")
        cwd = stdio_server.working_directory(self.scratch)

        uploads = [
            (empty_upload, "remote/empty.txt"),
            (
                os.path.relpath(nested / "every byte.bin", cwd),
                "remote/every byte.bin",
            ),
        ]
        downloads = [
            ("remote/every byte.bin", nested / "downloaded.bin", every_byte),
            ("remote/empty.txt", self.root / "downloaded empty.txt", b""),
            ("remote/every byte.bin", existing, every_byte),
        ]
        rejected = [
            ("Upload_File_from_Local", outside),
            ("Upload_File_from_Local", self.root / "escape" / "outside.txt"),
            ("Download_File_to_Local", self.root / ".." / "new.txt"),
            ("Download_File_to_Local", self.root / "escape" / "new.txt"),
        ]
        async with self.connect() as session:
            for local, remote in uploads:
                self.reply_to_upload(remote)
                error, text = await self.call(
                    session,
                    "Upload_File_from_Local",
                    {"local_path": str(local), "remote_path": remote},
                )
                self.assertFalse(error, text)
            for remote, local, data in downloads:
                self.reply_to_download(remote, data)
                error, text = await self.call(
                    session,
                    "Download_File_to_Local",
                    {"remote_path": remote, "local_path": str(local)},
                )
                self.assertFalse(error, text)
                self.assertEqual(
                    text, f"File downloaded successfully to: {local}"
                )
            sent = len(self.api.requests)
            for tool, local in rejected:
                error, text = await self.call(
                    session,
                    tool,
                    {"local_path": str(local), "remote_path": "remote/x"},
                )
                self.assertTrue(error)
                self.assertTrue(text.startswith("Local Path Error:"), text)
            # Rejected before any request.
            self.assertEqual(len(self.api.requests), sent)

        storage = [
            r for r in self.api.requests if r.url_path.startswith("/storage/")
        ]
        self.assertEqual(
            [r.body for r in storage if r.method == "PUT"], [b"", every_byte]
        )
        for _, local, data in downloads:
            self.assertEqual(local.read_bytes(), data)
        self.assertEqual(outside.read_bytes(), b"outside")
        self.assertFalse((self.scratch / "new.txt").exists())
        # Signed transfer URLs get no API key; API requests get this one.
        self.assertTrue(
            all("X-FilesAPI-Key" not in r.headers for r in storage)
        )
        self.assertEqual(
            {r.headers["X-FilesAPI-Key"] for r in self.api_requests()},
            {API_KEY},
        )
        # with_direct_connection_info is the SDK's own default, which the
        # server does not override.
        begin = [
            r.json for r in self.api_requests() if "begin_upload" in r.path
        ]
        self.assertEqual(
            begin,
            [
                {
                    "mkdir_parents": True,
                    "size": 0,
                    "with_direct_connection_info": True,
                },
                {
                    "mkdir_parents": True,
                    "size": len(every_byte),
                    "with_direct_connection_info": True,
                },
            ],
        )

    async def test_without_an_api_key_calls_fail_and_say_how_to_set_one(self):
        async with self.connect(api_key=None) as session:
            error, text = await self.call(session, "Find_User", {"id": 1})
        self.assertTrue(error)
        self.assertTrue(text.startswith("Authentication Error:"), text)
        self.assertIn("FILES_COM_API_KEY", text)
        self.assertEqual(self.api.requests, [])
        self.assertIn("FILES_COM_API_KEY is not set", self.stderr.read_text())

    @unittest.skipUnless(
        stdio_server.INSTALLED,
        "the console script exists once the package is installed",
    )
    async def test_console_script_serves_the_same_tools(self):
        self.api.reply_json([{"id": 1, "username": "pat"}])
        async with self.connect(stdio_server.console_command()) as session:
            tools = (await session.list_tools()).tools
            error, text = await self.call(session, "List_User")
        self.assertEqual(
            len(tools), len(GENERATED_TOOLS) + len(AUTHORED_TOOLS)
        )
        self.assertFalse(error)
        self.assertIn("| 1 | pat |", text)


if __name__ == "__main__":
    unittest.main()
