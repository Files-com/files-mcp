"""The framework releases whose internals files_com_mcp.patches adapts."""

from importlib.metadata import PackageNotFoundError, version

SUPPORTED_FRAMEWORK = {"fastmcp-slim": "3.4.10", "mcp": "1.30.0"}


def _installed(distribution):
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "not installed"


def require_supported_framework():
    """Raise unless the installed framework is the one the patches were
    verified against, rather than risk changing another's behavior
    unnoticed."""
    found = {name: _installed(name) for name in SUPPORTED_FRAMEWORK}
    unsupported = {
        name: installed
        for name, installed in found.items()
        if installed != SUPPORTED_FRAMEWORK[name]
    }
    if unsupported:
        raise RuntimeError(
            "this server supports only "
            + " and ".join(f"{n} {v}" for n, v in SUPPORTED_FRAMEWORK.items())
            + ", but found "
            + ", ".join(f"{n} {v}" for n, v in unsupported.items())
        )
