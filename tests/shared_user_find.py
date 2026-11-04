"""The Python MCP's consumer of the mock server's shared users-find scenario.

Run it through the mock server's with-scenario.rb, which starts a simulation
server, resets it with the scenario's fixtures and passes the server's
address, its placeholder key and the scenario file:

    ruby ../mock-server/with-scenario.rb --scenario users-find --out "$OUT" \
        -- python3 -m unittest -v tests.shared_user_find

The test starts this package as a child MCP STDIO server, pointed at the
simulator through the server's own FILES_COM_BASE_URL and FILES_COM_API_KEY,
and calls the generated Find_User tool: the installed SDK fetches the user
from the simulator over HTTP. The user to expect comes from the scenario's
expected_user. Its file name keeps it out of `unittest discover`; run
without the launcher's variables, it fails rather than skips.
"""

import json
import os
import sys
import unittest
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from mcp.types import TextContent

PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
LAUNCHER_VARIABLES = (
    "FILES_MOCK_SERVER_URL",
    "FILES_MOCK_API_KEY",
    "FILES_MOCK_SCENARIO_FILE",
)
# The scenario field naming the user to find: {"id", "username", "name"}.
EXPECTED_USER = "expected_user"


def table_cells(line):
    """The cells of one markdown table row, with the escapes the tools'
    table rendering adds (backslash before | and \\) removed."""
    cells, cell, chars = [], "", iter(line.strip()[1:])
    for char in chars:
        if char == "\\":
            cell += next(chars, "")
        elif char == "|":
            cells.append(cell.strip())
            cell = ""
        else:
            cell += char
    return cells


class TestSharedUserFind(unittest.IsolatedAsyncioTestCase):
    def launcher_inputs(self):
        missing = [name for name in LAUNCHER_VARIABLES if not os.getenv(name)]
        if missing:
            self.fail(
                "run this through the mock server's with-scenario.rb; "
                f"missing {', '.join(missing)}"
            )
        return {name: os.environ[name] for name in LAUNCHER_VARIABLES}

    def expected_user(self, scenario_file):
        scenario = json.loads(Path(scenario_file).read_text())
        user = scenario.get(EXPECTED_USER)
        if not (
            isinstance(user, dict)
            and type(user.get("id")) is int
            and all(
                isinstance(user.get(field), str) and user[field]
                for field in ("username", "name")
            )
        ):
            self.fail(
                f"{scenario_file} has no {EXPECTED_USER} with an integer id "
                "and a username and name"
            )
        return user

    async def test_find_user_returns_the_scenario_user(self):
        inputs = self.launcher_inputs()
        user = self.expected_user(inputs["FILES_MOCK_SCENARIO_FILE"])
        transport = StdioTransport(
            command=sys.executable,
            args=["-m", "files_com_mcp"],
            cwd=PROJECT_ROOT,
            env={
                "FILES_COM_BASE_URL": inputs["FILES_MOCK_SERVER_URL"],
                "FILES_COM_API_KEY": inputs["FILES_MOCK_API_KEY"],
            },
        )
        arguments = {"id": user["id"]}
        try:
            async with Client(
                transport, timeout=30, init_timeout=30
            ) as client:
                result = await client.call_tool("Find_User", arguments)
        finally:
            # Closing the client's end of STDIO is how the server stops.
            await transport.close()

        self.assertFalse(result.is_error)
        content = result.content[0]
        assert isinstance(content, TextContent)
        lines = content.text.split("\n")
        # Check the whole response's shape, not only that it is no error.
        self.assertEqual(lines[0], "User Response:", content.text)
        self.assertEqual(len(lines), 4, content.text)
        found = dict(zip(table_cells(lines[1]), table_cells(lines[3])))
        self.assertEqual(found.get("id"), str(user["id"]), content.text)
        self.assertEqual(found.get("username"), user["username"])
        self.assertEqual(found.get("name"), user["name"])


if __name__ == "__main__":
    unittest.main()
