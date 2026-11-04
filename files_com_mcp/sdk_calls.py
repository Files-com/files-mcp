"""Runs the Files.com SDK calls that tools make.

The SDK is synchronous. Each call runs in a worker thread, the way FastMCP
runs synchronous tools, so the server keeps handling protocol messages,
including other tool calls and cancellations, while a request or transfer
is under way. The worker runs in a copy of the tool call's context.

Each call also gets its own files_sdk.CancellationToken. When the MCP
request is cancelled, or the server stops because its client has gone, the
token stops the SDK operation and the tool waits for the worker to return
before it ends. No request or local file write outlives the tool call.

A failure raises ToolError, which clients receive as a tool result with
isError set and the message the tool gives.
"""

from typing import Any, Callable, TypeVar

import anyio
import anyio.to_thread
from fastmcp import Context
from fastmcp.exceptions import ToolError

import files_sdk
import files_sdk.error
from files_com_mcp.local_paths import LocalPathError

T = TypeVar("T")

MISSING_API_KEY_HINT = (
    " Set FILES_COM_API_KEY in the environment that the MCP client passes "
    "to this server."
)


async def call_files_api(
    context: Context, call: Callable[[dict[str, Any]], T]
) -> T:
    """Return call(options), run in a worker thread. options holds the
    configured API key (create_mcp() sets it from FILES_COM_API_KEY) and the
    call's cancellation token. Raises ToolError if the call fails."""
    api_key = files_sdk.get_api_key()
    token = files_sdk.CancellationToken()
    options = {"api_key": api_key, "cancel_token": token}
    try:
        return await _run_until_settled(lambda: call(options), token)
    except LocalPathError as error:
        raise ToolError(f"Local Path Error: {error}") from error
    except (
        files_sdk.error.AuthenticationError,
        files_sdk.error.NotAuthenticatedError,
    ) as error:
        hint = "" if api_key else MISSING_API_KEY_HINT
        raise ToolError(f"Authentication Error: {error}{hint}") from error
    except files_sdk.error.Error as error:
        raise ToolError(f"Files.com Error: {_described(error)}") from error
    except Exception as error:
        raise ToolError(f"General Exception: {error}") from error


def _described(error: files_sdk.error.Error) -> str:
    """The SDK error's message and, for a failed download that file storage
    explained, its explanation. The SDK adds storage's explanation to the
    error it raises as a note, with credentials in URLs already redacted,
    beside the download_request_status it read (see files_sdk.download).
    Notes on other errors are left out: they are the SDK's diagnostics for
    code that calls it, such as a checkpoint or cleanup failure."""
    text = str(error)
    if getattr(error, "download_request_status", None) is None:
        return text
    return "\n".join([text, *getattr(error, "__notes__", ())])


async def _run_until_settled(
    function: Callable[[], T], token: files_sdk.CancellationToken
) -> T:
    """function() in a worker thread. If this task is cancelled, cancel
    token, then wait for function to return before passing the
    cancellation on."""
    outcome: dict[str, Any] = {}
    finished = anyio.Event()

    async def work():
        # Shielded, so the task group waits for the worker even after the
        # request is cancelled.
        with anyio.CancelScope(shield=True):
            try:
                outcome["result"] = await anyio.to_thread.run_sync(function)
            except Exception as error:
                outcome["error"] = error
            finally:
                finished.set()

    async with anyio.create_task_group() as group:
        group.start_soon(work)
        try:
            await finished.wait()
        except anyio.get_cancelled_exc_class():
            token.cancel()
            raise

    if "error" in outcome:
        raise outcome["error"]
    return outcome["result"]
