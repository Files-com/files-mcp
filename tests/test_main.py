import io
import os
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from files_com_mcp import __main__
from tests import stdio_server

PROJECT_ROOT = str(Path(__file__).resolve().parents[1])


class DummySession:
    def __init__(self):
        self.verify = True


class DummyClient:
    def __init__(self):
        self.session = DummySession()


class TestMain(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_runtime_env_defaults_to_production(self):
        self.assertEqual(__main__._runtime_env(), "production")

    @patch.dict(
        os.environ,
        {"FILES_COM_ENV": "production", "FILES_COM_SSL_VERIFY": "false"},
        clear=True,
    )
    def test_rejects_insecure_ssl_in_production(self):
        with self.assertRaisesRegex(
            RuntimeError,
            "FILES_COM_SSL_VERIFY=false is not allowed in production",
        ):
            __main__._apply_ssl_verify_setting()

    @patch.dict(
        os.environ,
        {"FILES_COM_ENV": "staging", "FILES_COM_SSL_VERIFY": "false"},
        clear=True,
    )
    @patch("files_com_mcp.__main__.Api.client")
    def test_allows_insecure_ssl_outside_production(self, mock_client):
        client = DummyClient()
        mock_client.return_value = client

        __main__._apply_ssl_verify_setting()

        self.assertFalse(client.session.verify)

    @patch.dict(
        os.environ,
        {"FILES_COM_ENV": "production", "FILES_COM_SSL_VERIFY": "true"},
        clear=True,
    )
    @patch("files_com_mcp.__main__.Api.client")
    def test_allows_verified_ssl_in_production(self, mock_client):
        client = DummyClient()
        client.session.verify = False
        mock_client.return_value = client

        __main__._apply_ssl_verify_setting()

        self.assertTrue(client.session.verify)

    @patch("files_com_mcp.__main__.run_stdio")
    def test_refuses_to_start_with_an_sdk_that_cannot_cancel(self, run_stdio):
        released_sdk = SimpleNamespace(version="1.6.489")
        stderr = io.StringIO()
        with (
            patch("files_com_mcp.__main__.files_sdk", released_sdk),
            redirect_stderr(stderr),
            self.assertRaises(SystemExit) as exit,
        ):
            __main__.main([])
        self.assertEqual(exit.exception.code, 1)
        self.assertIn(
            "needs files-com 2.0 or newer, but files-com 1.6.489 is installed",
            stderr.getvalue(),
        )
        run_stdio.assert_not_called()

    @patch("files_com_mcp.__main__.run_stdio")
    @patch("files_com_mcp.framework.version")
    def test_refuses_to_start_with_an_unverified_framework(
        self, version, run_stdio
    ):
        version.side_effect = {"fastmcp-slim": "3.4.10", "mcp": "1.31.0"}.get
        stderr = io.StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit) as exit:
            __main__.main([])
        self.assertEqual(exit.exception.code, 1)
        self.assertIn(
            "supports only fastmcp-slim 3.4.10 and mcp 1.30.0, but found mcp 1.31.0",
            stderr.getvalue(),
        )
        run_stdio.assert_not_called()


class TestStdioStartup(unittest.IsolatedAsyncioTestCase):
    async def test_lists_tools_over_stdio(self):
        command = stdio_server.module_command()
        server = StdioServerParameters(
            command=command[0],
            args=command[1:],
            cwd=PROJECT_ROOT,
            env={"FILES_COM_SSL_VERIFY": "true"},
        )
        async with stdio_client(server) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                tools = (await session.list_tools()).tools
        self.assertTrue(tools)


if __name__ == "__main__":
    unittest.main()
