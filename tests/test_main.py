import os
import unittest
from unittest.mock import patch

from files_com_mcp import __main__


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


if __name__ == "__main__":
    unittest.main()
