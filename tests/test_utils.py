import unittest
import logging
from types import SimpleNamespace

import files_com_mcp
import files_sdk

class TestPathUtil(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Suppress logging to stdout/stderr, we will see errors at the end
        logging.getLogger("files_sdk").addHandler(logging.NullHandler())
        logging.getLogger("files_sdk").propagate = False

    def test_normalization_for_comparison(self):
        file1 = files_sdk.File("path1")
        file1.size = 12345 # type: ignore[attr-defined]
        file2 = files_sdk.File("path2")
        file2.size = 67890 # type: ignore[attr-defined]

        table = files_com_mcp.utils.object_list_to_markdown_table([file1, file2], ["path"])
        expected_table = "| path |\n| --- |\n| path1 |\n| path2 |"
        self.assertEqual(table, expected_table)

    def test_context_api_key_with_missing_request_context(self):
        context = SimpleNamespace(request_context=None)

        api_key = files_com_mcp.utils.context_api_key(context)

        self.assertEqual(api_key, "")

    def test_context_api_key_reads_session_snapshot(self):
        context = SimpleNamespace(
            request_context=SimpleNamespace(
                session=SimpleNamespace(_files_com_api_key="test-api-key")
            )
        )

        api_key = files_com_mcp.utils.context_api_key(context)

        self.assertEqual(api_key, "test-api-key")

if __name__ == '__main__':
    unittest.main()
