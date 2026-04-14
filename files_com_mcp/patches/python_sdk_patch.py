import files_com_mcp
from files_sdk.api_client import ApiClient

from files_com_mcp.sdk_request_mutator import apply_sdk_request_mutator

_original_request_headers = ApiClient.request_headers
_original_send_request = ApiClient.send_request


def patched_request_headers(self, api_key, session_id, language):
    headers = _original_request_headers(self, api_key, session_id, language)
    headers["User-Agent"] = "Files.com Python MCP SDK v{version}".format(
        version=files_com_mcp.__version__
    )

    return headers


def patched_send_request(
    self,
    method,
    path,
    api_key=None,
    session_id=None,
    language=None,
    headers=None,
    params=None,
):
    request_headers = dict(headers or {})
    request_headers = apply_sdk_request_mutator(
        method,
        path,
        api_key,
        session_id,
        language,
        request_headers,
        params,
    )

    return _original_send_request(
        self,
        method,
        path,
        api_key=api_key,
        session_id=session_id,
        language=language,
        headers=request_headers,
        params=params,
    )


ApiClient.request_headers = patched_request_headers
ApiClient.send_request = patched_send_request
