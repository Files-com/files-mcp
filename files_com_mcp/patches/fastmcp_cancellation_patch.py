"""Answers a cancelled request only once its handler has finished.

When a client cancels a request, mcp 1.30 cancels the request's handler and
at once sends the terminal "Request cancelled" error. A tool is then still
stopping its SDK call (see sdk_calls), so a client that carries on after
the error could overlap the end of that call. For requests to a FastMCP
server session, this makes cancelling only cancel the handler, and sends the
error when the handler returns, after its SDK call has stopped. The session
keeps reading and answering other requests meanwhile: cancelling no longer
waits on anything.

It replaces methods on the framework's classes (RequestResponder.cancel and
FastMCP's LowLevelServer._handle_request), not on one server. From the first
time create_mcp() runs (run_stdio() calls it) to the end of the process, it
therefore applies to every FastMCP server session in the process, including
those of other apps hosted beside this package.
Responders of other sessions, such as MCP clients', keep mcp's behavior.

This relies on mcp 1.30.0's RequestResponder and request dispatch and on
FastMCP 3.4.7's server session, which files_com_mcp.patches checks before
applying it.
"""

import anyio
from fastmcp.server.low_level import LowLevelServer, MiddlewareServerSession
from mcp.shared.session import RequestResponder
from mcp.types import ErrorData

_PENDING = "_files_com_cancellation_pending"
# Long enough for any live transport, short enough that a stuck one cannot
# hold up the handler's end.
_RESPONSE_SECONDS = 5

_original_cancel = RequestResponder.cancel
_original_handle_request = LowLevelServer._handle_request


async def _cancel(self):
    if (
        not isinstance(self._session, MiddlewareServerSession)
        or not self._entered
    ):
        return await _original_cancel(self)
    if self._completed:
        return  # Already answered; nothing is left to cancel.
    self._cancel_scope.cancel()
    setattr(self, _PENDING, True)


async def _handle_request(
    self, message, req, session, lifespan_context, raise_exceptions
):
    try:
        await _original_handle_request(
            self, message, req, session, lifespan_context, raise_exceptions
        )
    finally:
        if getattr(message, _PENDING, False):
            setattr(message, _PENDING, False)
            # Lets the request leave the session's in-flight requests.
            message._completed = True
            with (
                anyio.CancelScope(shield=True),
                anyio.move_on_after(_RESPONSE_SECONDS),
            ):
                try:
                    await session._send_response(
                        request_id=message.request_id,
                        response=ErrorData(
                            code=0, message="Request cancelled"
                        ),
                    )
                except (anyio.BrokenResourceError, anyio.ClosedResourceError):
                    pass  # The client has gone.


setattr(RequestResponder, "cancel", _cancel)
setattr(LowLevelServer, "_handle_request", _handle_request)
