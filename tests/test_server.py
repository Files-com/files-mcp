import os
import unittest
from unittest.mock import patch

from files_com_mcp import server


class DummyMCP:
    def __init__(self):
        self.run_calls = []

    def run(self, **kwargs):
        self.run_calls.append(kwargs)


class TestServerFactories(unittest.TestCase):
    @patch.dict(
        os.environ,
        {"FILES_COM_API_KEY": " test-api-key "},
        clear=True,
    )
    @patch("files_com_mcp.server.load_tools")
    @patch("files_com_mcp.server.files_sdk.set_api_key")
    def test_create_mcp_configures_environment_api_key(
        self, mock_set_api_key, _mock_load_tools
    ):
        server.create_mcp()

        mock_set_api_key.assert_called_once_with("test-api-key")

    def test_run_stdio_uses_factory_instance(self):
        dummy_mcp = DummyMCP()

        original_create_mcp = server.create_mcp
        server.create_mcp = lambda: dummy_mcp
        try:
            server.run_stdio()
        finally:
            server.create_mcp = original_create_mcp

        self.assertEqual(dummy_mcp.run_calls, [{"transport": "stdio"}])


if __name__ == "__main__":
    unittest.main()
