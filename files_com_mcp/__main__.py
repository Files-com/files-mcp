import argparse
import os

import files_sdk
from files_sdk.api import Api

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


def main():
    # For pointing to mock server for testing
    if os.getenv("FILES_COM_BASE_URL"):
        files_sdk.base_url = os.getenv("FILES_COM_BASE_URL")

    _apply_ssl_verify_setting()

    parser = argparse.ArgumentParser(
        description="Run the Files.com MCP server locally over STDIO. "
        "For network connections, use the Files.com hosted MCP service."
    )

    parser.parse_args()
    run_stdio()


if __name__ == "__main__":
    main()
