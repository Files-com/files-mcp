import argparse
import os

import files_sdk
from files_sdk.api import Api

from files_com_mcp.server import run_stdio, run_server


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

    parser = argparse.ArgumentParser(description="Run MCP server")

    parser.add_argument(
        "--mode",
        choices=["stdio", "server"],
        default="stdio",
        help="Transport mode: stdio or server (HTTP)",
    )

    parser.add_argument(
        "--port", type=int, default=8000, help="Port to use in server mode"
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind in server mode",
    )

    args = parser.parse_args()

    if args.mode == "stdio":
        run_stdio()
    elif args.mode == "server":
        run_server(port=args.port, host=args.host)


if __name__ == "__main__":
    main()
