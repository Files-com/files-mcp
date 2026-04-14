import os

from fastmcp.server.dependencies import get_http_headers
from mcp.server.session import ServerSession

_original_init = ServerSession.__init__
_original_getattribute = ServerSession.__getattribute__
_API_KEY_HEADER = "x-filesapi-key"
_SNAPSHOT_ATTR = "_files_com_api_key_snapshot"


def _files_com_api_key() -> str:
    headers = get_http_headers()

    header_api_key = ""
    if headers:
        header_api_key = headers.get(_API_KEY_HEADER, "")

        if not header_api_key:
            for key, value in headers.items():
                if isinstance(key, str) and key.lower() == _API_KEY_HEADER:
                    header_api_key = value
                    break

    api_key = str(header_api_key or "").strip()
    if api_key:
        return api_key

    return os.getenv("FILES_COM_API_KEY", "").strip()


def _files_com_api_key_for_session(session: ServerSession) -> str:
    api_key = _files_com_api_key()
    if api_key:
        return api_key

    try:
        return _original_getattribute(session, _SNAPSHOT_ATTR)
    except AttributeError:
        return ""


def patched_init(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)

    setattr(self, _SNAPSHOT_ATTR, _files_com_api_key())


def patched_getattribute(self, name):
    if name == "_files_com_api_key":
        return _files_com_api_key_for_session(self)

    return _original_getattribute(self, name)


ServerSession.__init__ = patched_init
ServerSession.__getattribute__ = patched_getattribute
