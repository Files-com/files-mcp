import files_com_mcp
from files_sdk.api_client import ApiClient

_original_request_headers = ApiClient.request_headers


def patched_request_headers(self, api_key, session_id, language):
    headers = _original_request_headers(self, api_key, session_id, language)
    headers["User-Agent"] = "Files.com Python MCP SDK v{version}".format(
        version=files_com_mcp.__version__
    )

    return headers


ApiClient.request_headers = patched_request_headers
