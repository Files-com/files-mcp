import json
import os
import queue
import signal
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path

import files_com_mcp
from tests import stdio_server
from tests.loopback_api import start_loopback_api

API_KEY = "mcpprotocolcanarykey"
# What these tests keep of a server's output; more fails the test rather
# than growing without bound. Server responses themselves are not limited.
CAPTURE_LIMIT = 8 * 1024 * 1024


class ServerProcess:
    """The server as a child process in its own process group. Its output
    is read on threads, so every wait has a deadline; what is kept of it is
    bounded; and cleanup kills the group if the server has not exited by
    itself."""

    def __init__(self, test, env, cwd, arguments=(), command=None):
        self.process = subprocess.Popen(
            [*(command or stdio_server.module_command()), *arguments],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            cwd=cwd,
            start_new_session=True,
        )
        assert (
            self.process.stdin and self.process.stdout and self.process.stderr
        )
        self.stdin = self.process.stdin
        self.lines = queue.Queue()
        self.stdout = []
        self.stderr = []
        self.captured = 0
        self.counting = threading.Lock()
        self.overflowed = False
        self.readers = [
            threading.Thread(
                target=self._read,
                args=(self.process.stdout, self.stdout, True),
                daemon=True,
            ),
            threading.Thread(
                target=self._read,
                args=(self.process.stderr, self.stderr, False),
                daemon=True,
            ),
        ]
        for reader in self.readers:
            reader.start()
        self.pending = []
        test.addCleanup(self.stop)

    def _read(self, stream, lines, notify):
        # Reads bounded chunks, so no line, however long, is held whole
        # past the limit, and keeps reading past it so the server never
        # blocks writing.
        partial = b""
        while chunk := stream.read1(65536):
            with self.counting:
                self.captured += len(chunk)
                over = self.captured > CAPTURE_LIMIT
            if over:
                self.overflowed = True
                partial = b""
                continue
            *complete, partial = (partial + chunk).split(b"\n")
            for line in complete:
                self._keep(line + b"\n", lines, notify)
        if partial and not self.overflowed:
            self._keep(partial, lines, notify)

    def _keep(self, line, lines, notify):
        lines.append(line)
        if notify:
            self.lines.put(line)

    def send(self, message):
        self.stdin.write(json.dumps(message).encode() + b"\n")
        self.stdin.flush()

    def request(self, request_id, method, params):
        self.send(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            }
        )

    def call_tool(self, request_id, name, arguments):
        self.request(
            request_id, "tools/call", {"name": name, "arguments": arguments}
        )

    def response(self, request_id, timeout=20):
        """The response to request_id, keeping other messages for later."""
        for message in self.pending:
            if message.get("id") == request_id:
                self.pending.remove(message)
                return message
        deadline = time.monotonic() + timeout
        while True:
            if self.overflowed:
                raise AssertionError(
                    "the server wrote more than CAPTURE_LIMIT"
                )
            line = self.lines.get(timeout=max(0, deadline - time.monotonic()))
            message = json.loads(line)
            if message.get("id") == request_id and "method" not in message:
                return message
            self.pending.append(message)

    def initialize(self):
        self.request(
            0,
            "initialize",
            {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "files-mcp-tests", "version": "1"},
            },
        )
        result = self.response(0)["result"]
        self.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return result

    def close_input(self):
        self.stdin.close()

    def wait(self, timeout):
        status = self.process.wait(timeout)
        for reader in self.readers:
            reader.join(timeout)
        return status

    def stop(self):
        if self.process.poll() is None:
            os.killpg(self.process.pid, signal.SIGKILL)
        self.process.wait(10)
        for reader in self.readers:
            reader.join(10)
        for stream in (self.stdin, self.process.stdout, self.process.stderr):
            if stream is not None and not stream.closed:
                stream.close()
        if any(reader.is_alive() for reader in self.readers):
            raise AssertionError("the server's output was not read to its end")


def text_of(response):
    [content] = response["result"]["content"]
    return content["text"]


class TestStdioProtocol(unittest.TestCase):
    """The server's standard output carries only protocol messages, and a
    slow tool call neither holds up others nor outlives its request or
    the connection."""

    def setUp(self):
        self.api = start_loopback_api(self)
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name).resolve()
        self.root = self.scratch / "root"
        self.root.mkdir()

    def start(self, arguments=(), command=None, **settings):
        settings = {
            "FILES_COM_API_KEY": API_KEY,
            "FILES_COM_BASE_URL": self.api.url,
            "FILES_COM_LOCAL_ROOT": str(self.root),
            **settings,
        }
        return ServerProcess(
            self,
            stdio_server.environment(**settings),
            stdio_server.working_directory(self.scratch),
            arguments,
            command,
        )

    def assert_only_protocol_on_stdout(self, server):
        self.assertFalse(server.overflowed)
        self.assertTrue(server.stdout)
        for line in server.stdout:
            self.assertEqual(json.loads(line)["jsonrpc"], "2.0", line)
        output = b"".join(server.stdout + server.stderr).decode()
        self.assertNotIn(API_KEY, output)

    def test_slow_calls_do_not_hold_up_others_and_stop_when_cancelled(self):
        slow = self.api.hold_json([{"id": 1, "username": "slow"}])
        server = self.start()
        initialized = server.initialize()
        self.assertEqual(initialized["protocolVersion"], "2025-11-25")

        server.call_tool(2, "List_User", {})
        self.assertTrue(slow.arrived.wait(10))
        self.api.reply_json({"id": 2, "username": "quick"})
        server.call_tool(3, "Find_User", {"id": 2})
        quick = server.response(3)
        self.assertFalse(quick["result"]["isError"])
        self.assertIn("quick", text_of(quick))

        server.send(
            {
                "jsonrpc": "2.0",
                "method": "notifications/cancelled",
                "params": {"requestId": 2, "reason": "test"},
            }
        )
        # Cancelling stopped the SDK request: its connection closed.
        self.assertTrue(slow.client_closed.wait(10))
        cancelled = server.response(2)
        self.assertNotIn("result", cancelled)

        server.close_input()
        self.assertEqual(server.wait(20), 0)
        self.assertEqual(len(self.api.requests), 2)
        self.assert_only_protocol_on_stdout(server)

    def test_cancellation_is_answered_once_the_call_has_stopped(self):
        # The SDK call takes a while to stop once cancelled, as a transfer
        # can; other requests are answered meanwhile.
        markers = self.scratch / "markers"
        markers.mkdir()
        server = self.start(command=stdio_server.delayed_sdk_command(markers))
        server.initialize()
        server.call_tool(2, "Find_User", {"id": 1})
        self.wait_for(markers / "started.json")

        cancel = {
            "jsonrpc": "2.0",
            "method": "notifications/cancelled",
            "params": {"requestId": 2, "reason": "test"},
        }
        server.send(cancel)
        self.wait_for(markers / "cancel_seen.json")
        server.send(cancel)  # A repeated cancellation changes nothing.
        server.request(3, "ping", {})
        pong = server.response(3)
        self.assertEqual(pong["result"], {})
        self.assertFalse((markers / "settled.json").exists())

        cancelled = server.response(2)
        self.assertTrue((markers / "settled.json").exists())
        self.assertEqual(cancelled["error"]["message"], "Request cancelled")

        server.close_input()
        self.assertEqual(server.wait(20), 0)
        answers = [json.loads(line) for line in server.stdout]
        self.assertEqual(sum(a.get("id") == 2 for a in answers), 1)
        self.assert_only_protocol_on_stdout(server)

    def wait_for(self, path, timeout=10):
        deadline = time.monotonic() + timeout
        while not path.exists():
            if time.monotonic() > deadline:
                self.fail(f"{path.name} did not appear in {timeout} seconds")
            time.sleep(0.01)

    def test_closing_input_stops_a_download_before_the_server_exits(self):
        destination = self.root / "download.bin"
        self.api.reply_json(
            {
                "path": "big.bin",
                "type": "file",
                "size": 16,
                "download_uri": self.api.url + "/storage/big.bin",
            }
        )
        held = self.api.hold(200, b"0123456789abcdef")
        server = self.start()
        server.initialize()
        server.call_tool(
            2,
            "Download_File_to_Local",
            {"remote_path": "big.bin", "local_path": str(destination)},
        )
        self.assertTrue(held.arrived.wait(10))

        server.close_input()
        self.assertEqual(server.wait(20), 0)
        # The download's connection closed as the server stopped, and it
        # left nothing behind.
        self.assertTrue(held.client_closed.wait(10))
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertFalse(
            any(
                json.loads(line).get("id") == 2
                and "result" in json.loads(line)
                for line in server.stdout
            )
        )
        self.assert_only_protocol_on_stdout(server)

    def test_refuses_to_start_with_invalid_settings_or_network_options(self):
        for arguments, settings, status, message in (
            (
                (),
                {"FILES_COM_LOCAL_ROOT": "relative/path"},
                1,
                "Invalid FILES_COM_LOCAL_ROOT",
            ),
            (
                (),
                {"FILES_COM_SSL_VERIFY": "false"},
                1,
                "not allowed in production",
            ),
            (("--transport", "http"), {}, 2, "unrecognized arguments"),
            (("--port", "8000"), {}, 2, "unrecognized arguments"),
        ):
            with self.subTest(arguments=arguments, settings=settings):
                server = self.start(arguments, **settings)
                server.close_input()
                self.assertEqual(server.wait(30), status)
                self.assertEqual(server.stdout, [])
                self.assertIn(message, b"".join(server.stderr).decode())

    def test_reports_its_version(self):
        server = self.start(("--version",))
        self.assertEqual(server.wait(30), 0)
        self.assertEqual(
            b"".join(server.stdout).decode(),
            f"files-com-mcp {files_com_mcp.__version__}\n",
        )


if __name__ == "__main__":
    unittest.main()
