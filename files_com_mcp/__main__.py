import argparse
import os
import sys

import files_sdk
from files_sdk.api import Api

import files_com_mcp
from files_com_mcp.local_paths import LocalPathError, configured_local_root
from files_com_mcp.framework import require_supported_framework
from files_com_mcp.server import run_stdio


def _get_bool_env(name: str) -> bool | None:
    value = os.getenv(name)
    if value is None:
        return None

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value for {name}: {value}")


def _runtime_env() -> str:
    return os.getenv("FILES_COM_ENV", "production").strip().lower()


def _apply_ssl_verify_setting() -> None:
    ssl_verify = _get_bool_env("FILES_COM_SSL_VERIFY")
    if ssl_verify is None:
        return

    if not ssl_verify and _runtime_env() == "production":
        raise RuntimeError(
            "FILES_COM_SSL_VERIFY=false is not allowed in production"
        )

    Api.client().session.verify = ssl_verify


def _check_sdk() -> None:
    # The tools cancel SDK operations when their MCP request is cancelled.
    if not hasattr(files_sdk, "CancellationToken"):
        raise RuntimeError(
            "this server needs files-com 2.0 or newer, but files-com "
            f"{files_sdk.version} is installed"
        )


def _configure() -> None:
    """Apply the environment's settings, raising if any is invalid."""
    _check_sdk()
    require_supported_framework()
    # For pointing to mock server for testing
    if os.getenv("FILES_COM_BASE_URL"):
        files_sdk.base_url = os.getenv("FILES_COM_BASE_URL")

    check_modification_time = _get_bool_env(
        "FILES_COM_CHECK_DOWNLOAD_MODIFICATION_TIME"
    )
    files_sdk.check_download_modification_time = (
        True if check_modification_time is None else check_modification_time
    )

    _apply_ssl_verify_setting()
    configured_local_root()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="files-com-mcp",
        description="Run the Files.com MCP server locally over STDIO. "
        "For network connections, use the Files.com hosted MCP service.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {files_com_mcp.__version__}",
    )
    parser.parse_args(argv)

    try:
        _configure()
    except (LocalPathError, RuntimeError, ValueError) as error:
        parser.exit(1, f"{parser.prog}: error: {error}\n")

    # Standard output carries the protocol, so diagnostics go to stderr.
    if not os.getenv("FILES_COM_API_KEY", "").strip():
        print(
            f"{parser.prog}: warning: FILES_COM_API_KEY is not set, so tool "
            "calls will fail. Set it in the environment that the MCP client "
            "passes to this server.",
            file=sys.stderr,
        )

    run_stdio()


if __name__ == "__main__":
    main()
