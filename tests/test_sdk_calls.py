"""Concurrency guarantees of files_com_mcp.sdk_calls.

A blocking SDK call must not block the event loop, and a cancelled tool call
must wait for its worker to return before the cancellation passes on.
"""

import asyncio
import threading
import time
import unittest
from typing import cast
from unittest import mock

from fastmcp import Context

import files_sdk
from files_com_mcp import sdk_calls


async def wait_for_event(event, limit=2.0):
    deadline = time.monotonic() + limit
    while not event.is_set() and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    return event.is_set()


class FakeCancellationToken:
    def __init__(self):
        self.cancelled = threading.Event()

    def cancel(self):
        self.cancelled.set()


class _NoContext:
    """A tool context outside any MCP session: the call uses the module's
    API key."""

    request_context = None


NO_CONTEXT = cast(Context, _NoContext())


@mock.patch.object(files_sdk, "get_api_key", lambda: "key")
class TestCallFilesApi(unittest.IsolatedAsyncioTestCase):
    async def test_event_loop_runs_while_the_call_blocks(self):
        started, release = threading.Event(), threading.Event()

        def call(options):
            started.set()
            release.wait(5)
            return options["api_key"]

        task = asyncio.create_task(sdk_calls.call_files_api(NO_CONTEXT, call))
        began = time.monotonic()
        self.assertTrue(await wait_for_event(started))
        # Run inline, the call would hold the loop for its full 5 s wait.
        self.assertLess(time.monotonic() - began, 2.0)
        self.assertFalse(task.done())
        release.set()
        self.assertEqual(await task, "key")

    async def test_cancelled_call_waits_for_its_worker(self):
        started, release, returned = (threading.Event() for _ in range(3))

        def call(options):
            started.set()
            release.wait(5)
            returned.set()
            return "done"

        task = asyncio.create_task(sdk_calls.call_files_api(NO_CONTEXT, call))
        self.assertTrue(await wait_for_event(started))
        task.cancel()
        await asyncio.sleep(0.1)
        self.assertFalse(task.done())
        release.set()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(returned.is_set())

    async def test_cancellation_stops_a_call_with_sdk_token(self):
        started, returned = threading.Event(), threading.Event()
        seen = {}

        def call(options):
            seen.update(options)
            started.set()
            # An SDK operation that honors its token stops when cancelled.
            options["cancel_token"].cancelled.wait(5)
            returned.set()
            return "stopped"

        with mock.patch.object(
            files_sdk, "CancellationToken", FakeCancellationToken
        ):
            task = asyncio.create_task(
                sdk_calls.call_files_api(NO_CONTEXT, call)
            )
            self.assertTrue(await wait_for_event(started))
            began = time.monotonic()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(returned.is_set())
        self.assertLess(time.monotonic() - began, 2.0)
        self.assertEqual(seen["api_key"], "key")
        self.assertTrue(seen["cancel_token"].cancelled.is_set())


if __name__ == "__main__":
    unittest.main()
