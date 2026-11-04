import asyncio
import os
import unittest
from typing import cast
from unittest.mock import patch

import anyio
from fastmcp import Client, Context
from fastmcp.server.dependencies import get_context
from mcp.types import TextContent

import files_sdk
import files_sdk.error
from files_com_mcp.sdk_calls import call_files_api
from files_com_mcp.sdk_request_mutator import set_sdk_request_mutator
from files_com_mcp.server import create_mcp
from tests.loopback_api import serve_loopback_api

USERS = [{"id": 1, "username": "pat"}]


class TestResponsiveness(unittest.IsolatedAsyncioTestCase):
    """SDK calls run off the event loop, so a slow request does not hold
    up the server, and a cancelled call stops its SDK operation before it
    ends."""

    def setUp(self):
        self.api = serve_loopback_api(self)

    async def test_other_calls_complete_while_a_request_waits(self):
        slow = self.api.hold_json(USERS)
        async with Client(create_mcp()) as client:
            slow_call = asyncio.create_task(client.call_tool("List_User", {}))
            self.assertTrue(await asyncio.to_thread(slow.arrived.wait, 10))

            self.api.reply_json({"id": 2, "username": "robin"})
            quick = await asyncio.wait_for(
                client.call_tool("Find_User", {"id": 2}), 10
            )
            self.assertIn("robin", text(quick))
            self.assertFalse(slow_call.done())

            slow.release()
            listed = await asyncio.wait_for(slow_call, 10)
        self.assertIn("pat", text(listed))

    async def test_cancelled_call_stops_its_request_before_it_ends(self):
        held = self.api.hold_json(USERS)
        worker = {}

        def list_users(options):
            try:
                return files_sdk.user.list({}, options)
            except BaseException as error:
                worker["error"] = error
                raise
            finally:
                worker["returned"] = True

        scope = anyio.CancelScope()

        async def cancel_once_sent():
            await asyncio.to_thread(held.arrived.wait, 10)
            scope.cancel()

        canceller = asyncio.create_task(cancel_once_sent())
        with patch.object(files_sdk, "the_api_key", "mcptestkey"), scope:
            await call_files_api(cast(Context, _NoContext()), list_users)
            self.fail("The call was not cancelled")
        await canceller
        self.assertTrue(scope.cancelled_caught)

        # The worker returned, having stopped the request, before the call
        # ended; the server then saw the connection close.
        self.assertTrue(worker.get("returned"))
        self.assertIsInstance(
            worker["error"], files_sdk.error.OperationCancelledError
        )
        self.assertTrue(await asyncio.to_thread(held.client_closed.wait, 5))
        self.assertEqual(len(self.api.requests), 1)

    async def test_concurrent_calls_use_configured_key_and_own_context(self):
        seen = []

        def mutator(
            method, path, api_key, session_id, language, headers, params
        ):
            # The worker runs in the context of the tool call that made it.
            seen.append((api_key, get_context().session))
            headers["X-Mutated"] = "yes"
            return headers

        set_sdk_request_mutator(mutator)
        self.addCleanup(set_sdk_request_mutator, None)
        # The server takes the key in its environment, without the spaces
        # around it, when it is created.
        with patch.dict(os.environ, {"FILES_COM_API_KEY": " mcptestkey "}):
            server = create_mcp()
        holds = [self.api.hold_json(USERS), self.api.hold_json(USERS)]
        clients = []
        for _ in range(2):
            client = Client(server)
            await client.__aenter__()
            self.addAsyncCleanup(client.__aexit__, None, None, None)
            clients.append(client)

        # Removing it from the environment afterwards does not change that.
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        del os.environ["FILES_COM_API_KEY"]
        calls = [
            asyncio.create_task(client.call_tool("List_User", {}))
            for client in clients
        ]
        for hold in holds:
            self.assertTrue(await asyncio.to_thread(hold.arrived.wait, 10))
        # Both requests are in flight together.
        self.assertEqual(len(self.api.requests), 2)
        self.assertFalse(any(call.done() for call in calls))
        for hold in holds:
            hold.release()
        results = await asyncio.wait_for(asyncio.gather(*calls), 10)
        self.assertTrue(all("pat" in text(r) for r in results))

        sent = [r.headers["X-FilesAPI-Key"] for r in self.api.requests]
        self.assertEqual(sent, ["mcptestkey", "mcptestkey"])
        self.assertEqual(
            [key for key, _ in seen], ["mcptestkey", "mcptestkey"]
        )
        # Each worker saw the session of its own call.
        self.assertEqual(len({id(session) for _, session in seen}), 2)
        self.assertTrue(
            all(r.headers["X-Mutated"] == "yes" for r in self.api.requests)
        )

    async def test_mutator_runs_once_per_call_across_retries(self):
        calls = []

        def mutator(
            method, path, api_key, session_id, language, headers, params
        ):
            calls.append((method, path, dict(params or {})))
            if params is not None:
                params["added_by_mutator"] = True
            return headers

        set_sdk_request_mutator(mutator)
        self.addCleanup(set_sdk_request_mutator, None)
        self.api.disconnect()
        self.api.reply_json(USERS)
        with patch.object(files_sdk, "max_network_retries", 1):
            async with Client(create_mcp()) as client:
                result = await client.call_tool("List_User", {"per_page": 5})
        self.assertIn("pat", text(result))
        self.assertEqual(len(self.api.requests), 2)
        self.assertEqual(calls, [("GET", "/users", {"per_page": 5})])


def text(result):
    [content] = result.content
    assert isinstance(content, TextContent)
    return content.text


class _NoContext:
    """A tool context outside any MCP session: the call uses the module's
    API key."""

    request_context = None


if __name__ == "__main__":
    unittest.main()
