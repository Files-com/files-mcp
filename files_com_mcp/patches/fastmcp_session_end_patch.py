"""Cancels the tool calls still running when a session's input ends.

When its client's connection closes, the MCP SDK's server loop cancels the
requests it is still handling, so none outlives its client. FastMCP 3.4.7
runs its own copy of that loop, without that step: after a STDIO client
closes the server's input, a transfer would carry on to the end for a
client that has gone. This restores the step in FastMCP's loop, which runs
each request's handler in the task group it keeps on the session. Each tool
then stops its SDK operation and waits for it (see sdk_calls).

It replaces a property of FastMCP's MiddlewareServerSession class, not of one
server. From the first time create_mcp() runs (run_stdio() calls it) to the
end of the process, it therefore applies to every FastMCP server session in
the process, including those of other apps hosted beside this package.
"""

from fastmcp.server.low_level import MiddlewareServerSession

_original_incoming_messages = MiddlewareServerSession.incoming_messages


class _CancelHandlersAtEnd:
    """The session's incoming messages. Once they end, the handlers still
    running are cancelled."""

    def __init__(self, session, messages):
        self._session = session
        self._messages = messages

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self._messages.__anext__()
        except StopAsyncIteration:
            handlers = getattr(self._session, "_subscription_task_group", None)
            if handlers is not None:
                handlers.cancel_scope.cancel()
            raise

    def __getattr__(self, name):
        return getattr(self._messages, name)


def _incoming_messages(self):
    messages = _original_incoming_messages.__get__(self, type(self))
    return _CancelHandlersAtEnd(self, messages)


setattr(
    MiddlewareServerSession, "incoming_messages", property(_incoming_messages)
)
