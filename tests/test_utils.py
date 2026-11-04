import unittest
import logging

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
        file1.size = 12345  # type: ignore[attr-defined]
        file2 = files_sdk.File("path2")
        file2.size = 67890  # type: ignore[attr-defined]

        table = files_com_mcp.utils.object_list_to_markdown_table(
            [file1, file2], ["path"]
        )
        expected_table = "| path |\n| --- |\n| path1 |\n| path2 |"
        self.assertEqual(table, expected_table)

    def test_selected_fields_exclude_sdk_options(self):
        user = files_sdk.User(
            {"id": 1, "username": "user@example.test"},
            {"foo": "bar"},
        )
        user.non_default_field = "visible"  # type: ignore[attr-defined]

        table = files_com_mcp.utils.object_list_to_markdown_table(
            [user],
            ["id", "username"],
            fields=[
                "username",
                "non_default_field",
                "options",
                "__dict__",
            ],
        )

        expected_table = (
            "| username | non_default_field |\n"
            "| --- | --- |\n"
            "| user@example.test | visible |"
        )
        self.assertEqual(table, expected_table)

    def test_default_columns_exclude_sdk_options(self):
        # A record the SDK decoded keeps the options of the call that read it,
        # such as the API key and cancellation token a tool call passes.
        user = files_sdk.User(
            {"id": 1, "username": "user@example.test"},
            {
                "api_key": "sentinel-api-key",
                "cancel_token": files_sdk.CancellationToken(),
            },
        )

        # Default columns, such as the parameter names a record without
        # declared properties falls back to, can name them too.
        table = files_com_mcp.utils.object_list_to_markdown_table(
            [user], ["id", "options", "username", "__dict__"]
        )

        expected_table = (
            "| id | username |\n| --- | --- |\n| 1 | user@example.test |"
        )
        self.assertEqual(table, expected_table)
        self.assertNotIn("sentinel-api-key", table)


if __name__ == "__main__":
    unittest.main()
