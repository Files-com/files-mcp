import os
from typing import cast
import unittest
from unittest.mock import patch

from files_com_mcp.patches import fastmcp_settings_patch


class TestFastMcpSettingsPatch(unittest.TestCase):
    @patch.dict(os.environ, {"FILES_COM_API_KEY": "env-api-key"}, clear=True)
    @patch("files_com_mcp.patches.fastmcp_settings_patch.get_http_headers")
    def test_prefers_header_key(self, mock_get_http_headers):
        mock_get_http_headers.return_value = {"x-filesapi-key": "header-api-key"}

        api_key = fastmcp_settings_patch._files_com_api_key()

        self.assertEqual(api_key, "header-api-key")

    @patch.dict(os.environ, {"FILES_COM_API_KEY": "env-api-key"}, clear=True)
    @patch("files_com_mcp.patches.fastmcp_settings_patch.get_http_headers")
    def test_falls_back_to_env_when_header_missing(self, mock_get_http_headers):
        mock_get_http_headers.return_value = {}

        api_key = fastmcp_settings_patch._files_com_api_key()

        self.assertEqual(api_key, "env-api-key")

    @patch.dict(os.environ, {}, clear=True)
    @patch("files_com_mcp.patches.fastmcp_settings_patch.get_http_headers")
    def test_empty_when_no_header_or_env(self, mock_get_http_headers):
        mock_get_http_headers.return_value = {}

        api_key = fastmcp_settings_patch._files_com_api_key()

        self.assertEqual(api_key, "")

    @patch.dict(os.environ, {"FILES_COM_API_KEY": "env-api-key"}, clear=True)
    @patch("files_com_mcp.patches.fastmcp_settings_patch.get_http_headers")
    def test_accepts_case_variant_header_name(self, mock_get_http_headers):
        mock_get_http_headers.return_value = {"X-FilesApi-Key": "header-api-key"}

        api_key = fastmcp_settings_patch._files_com_api_key()

        self.assertEqual(api_key, "header-api-key")

    @patch.dict(os.environ, {}, clear=True)
    @patch("files_com_mcp.patches.fastmcp_settings_patch.get_http_headers")
    def test_session_prefers_current_header_over_snapshot(self, mock_get_http_headers):
        class DummySession:
            pass

        session = DummySession()
        setattr(session, "_files_com_api_key_snapshot", "snapshot-api-key")

        mock_get_http_headers.return_value = {"x-filesapi-key": "header-api-key"}

        api_key = fastmcp_settings_patch._files_com_api_key_for_session(
            cast(fastmcp_settings_patch.ServerSession, session)
        )

        self.assertEqual(api_key, "header-api-key")

    @patch.dict(os.environ, {}, clear=True)
    @patch("files_com_mcp.patches.fastmcp_settings_patch.get_http_headers")
    def test_session_falls_back_to_snapshot_when_current_header_missing(
        self, mock_get_http_headers
    ):
        class DummySession:
            pass

        session = DummySession()
        setattr(session, "_files_com_api_key_snapshot", "snapshot-api-key")

        mock_get_http_headers.return_value = {}

        api_key = fastmcp_settings_patch._files_com_api_key_for_session(
            cast(fastmcp_settings_patch.ServerSession, session)
        )

        self.assertEqual(api_key, "snapshot-api-key")


if __name__ == "__main__":
    unittest.main()
