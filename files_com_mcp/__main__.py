import argparse
import os
import files_sdk
from files_com_mcp.server import run_stdio, run_server


def main():
    # For pointing to mock server for testing
    if os.getenv("FILES_COM_BASE_URL"):
        files_sdk.base_url = os.getenv("FILES_COM_BASE_URL")

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

    args = parser.parse_args()

    if args.mode == "stdio":
        run_stdio()
    elif args.mode == "server":
        run_server(port=args.port)


if __name__ == "__main__":
    main()
