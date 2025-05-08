import unittest
import logging
import json

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

if __name__ == '__main__':
    unittest.main()

