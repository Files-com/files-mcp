from files_com_mcp.framework import require_supported_framework

# The patches adapt internals of exact framework releases.
require_supported_framework()

from . import fastmcp_cancellation_patch  # noqa: E402,F401
from . import fastmcp_session_end_patch  # noqa: E402,F401
from . import python_sdk_patch  # noqa: E402,F401
