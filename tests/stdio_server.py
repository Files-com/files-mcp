"""How the tests start the server the way an MCP client does: as a child
process that speaks MCP over its standard input and output.

When the package under test is installed (it is not imported from the
directory holding these tests), the server runs from a directory without
its source and, as python -m, in isolated mode (-I), so neither
PYTHONPATH, the user's site-packages nor a source tree can stand in for the
installed package. Otherwise it runs from the source directory.
"""

import os
import sys
import sysconfig
from pathlib import Path

import files_com_mcp

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTALLED = (
    not Path(files_com_mcp.__file__).resolve().is_relative_to(PROJECT_ROOT)
)


def recorded(command):
    """command, started through child_ledger.py when a qualification run
    keeps a ledger of the server children (FILES_MCP_CHILD_LEDGER)."""
    ledger = os.environ.get("FILES_MCP_CHILD_LEDGER")
    if not ledger:
        return command
    launcher = Path(__file__).with_name("child_ledger.py")
    return [sys.executable, "-I", str(launcher), ledger, *command]


def module_command():
    """python -m files_com_mcp"""
    if INSTALLED:
        return recorded([sys.executable, "-I", "-m", "files_com_mcp"])
    return recorded([sys.executable, "-m", "files_com_mcp"])


def console_command():
    """The files-com-mcp console script of the installed package."""
    name = "files-com-mcp.exe" if os.name == "nt" else "files-com-mcp"
    return recorded([str(Path(sysconfig.get_path("scripts")) / name)])


def delayed_sdk_command(markers):
    """The server with a slow-to-cancel SDK call (delayed_sdk_server.py)."""
    script = str(Path(__file__).with_name("delayed_sdk_server.py"))
    if INSTALLED:
        return recorded([sys.executable, "-I", script, str(markers)])
    return recorded([sys.executable, script, str(markers), str(PROJECT_ROOT)])


def working_directory(scratch):
    return scratch if INSTALLED else PROJECT_ROOT


def environment(**settings):
    """The child's whole environment: what it needs to run, and settings.
    A setting of None is left out."""
    names = ("PATH", "HOME", "SYSTEMROOT", "TMPDIR", "TEMP", "TMP")
    env = {name: os.environ[name] for name in names if name in os.environ}
    env.update(
        {name: value for name, value in settings.items() if value is not None}
    )
    return env
