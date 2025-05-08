from mcp.server.session import ServerSession
import os

_original_init = ServerSession.__init__


def patched_init(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)

    # Inject your custom attributes
    self._files_com_api_key = os.getenv("FILES_COM_API_KEY", "").strip()


ServerSession.__init__ = patched_init
