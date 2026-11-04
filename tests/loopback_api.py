"""A local stand-in for the Files.com API, so tests run the SDK's real HTTP
stack against scripted responses and see every request it sends."""

import json
import os
import select
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from urllib.parse import parse_qsl, urlsplit

API_PREFIX = "/api/rest/v1"


class RecordedRequest:
    def __init__(self, method, target, headers, body):
        url = urlsplit(target)
        self.method = method
        # url_path is the whole path, for requests elsewhere, such as to a
        # signed transfer URL; path is the part after the API prefix.
        self.url_path = url.path
        self.path = url.path[len(API_PREFIX) :]
        self.query = dict(parse_qsl(url.query, keep_blank_values=True))
        self.headers = headers
        self.body = body

    @property
    def json(self):
        is_json = self.headers.get("Content-Type", "").startswith(
            "application/json"
        )
        return json.loads(self.body) if self.body and is_json else None


class Hold:
    """A response that waits for release(). While it waits, it notices the
    client closing the connection, as a cancelled SDK operation does."""

    def __init__(self, status, headers, body):
        self.response = (status, headers, body)
        self.arrived = threading.Event()
        self.released = threading.Event()
        self.client_closed = threading.Event()

    def release(self):
        self.released.set()


DISCONNECT = "disconnect"


class LoopbackApi:
    def __init__(self):
        self.requests = []
        self.responses = []
        self.errors = []
        self.holds = []
        self._arrived = threading.Condition()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler())
        self.server.daemon_threads = False
        self.url = "http://127.0.0.1:{}".format(self.server.server_port)

    def reply(self, status=200, body=b"", headers=None):
        """Answer the next request."""
        self.responses.append((status, dict(headers or {}), body))

    def reply_json(self, value, status=200, headers=None):
        headers = {"Content-Type": "application/json", **(headers or {})}
        self.reply(status, json.dumps(value).encode(), headers)

    def hold(self, status=200, body=b"", headers=None):
        """Answer the next request once the returned Hold is released."""
        hold = Hold(status, dict(headers or {}), body)
        self.responses.append(hold)
        self.holds.append(hold)
        return hold

    def hold_json(self, value, status=200, headers=None):
        headers = {"Content-Type": "application/json", **(headers or {})}
        return self.hold(status, json.dumps(value).encode(), headers)

    def disconnect(self):
        """Close the connection of the next request without answering."""
        self.responses.append(DISCONNECT)

    def wait_for_requests(self, count, timeout=10):
        with self._arrived:
            self._arrived.wait_for(
                lambda: len(self.requests) >= count, timeout
            )
        return self.requests

    def _handler(self):
        api = self

        class Handler(BaseHTTPRequestHandler):
            def serve(self):
                length = int(self.headers.get("Content-Length") or 0)
                request = RecordedRequest(
                    self.command,
                    self.path,
                    self.headers,
                    self.rfile.read(length),
                )
                with api._arrived:
                    api.requests.append(request)
                    script = api.responses.pop(0) if api.responses else None
                    api._arrived.notify_all()
                if script is DISCONNECT:
                    self.close_connection = True
                    return
                if script is None:
                    api.errors.append(f"Unexpected request: {self.path}")
                    script = (500, {}, b"no scripted response")
                if isinstance(script, Hold):
                    script.arrived.set()
                    if not self.wait_for_release(script):
                        self.close_connection = True
                        return
                    script = script.response
                status, headers, body = script
                try:
                    self.send_response(status)
                    for name, value in headers.items():
                        self.send_header(name, value)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except ConnectionError:
                    self.close_connection = True  # The client gave up.

            def wait_for_release(self, hold):
                """True once hold is released; False if the client closes
                the connection first."""
                connection = self.connection
                # Answer eventually, so a client that never lets go cannot
                # keep the test waiting.
                deadline = time.monotonic() + 20
                while not hold.released.wait(0.02):
                    if time.monotonic() > deadline:
                        break
                    readable, _, _ = select.select([connection], [], [], 0)
                    if readable:
                        try:
                            data = connection.recv(1, socket.MSG_PEEK)
                        except OSError:
                            data = b""
                        if not data:
                            hold.client_closed.set()
                            return False
                return True

            do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = serve

            def log_message(self, format, *args):
                pass

        return Handler


def start_loopback_api(test_case):
    """A new LoopbackApi that serves until the test ends. Cleanup releases
    anything still held, then waits for the server and its handler threads
    to stop."""
    api = LoopbackApi()
    thread = threading.Thread(
        target=api.server.serve_forever, kwargs={"poll_interval": 0.05}
    )
    thread.start()

    def stop():
        for hold in api.holds:
            hold.release()
        api.server.shutdown()
        api.server.server_close()
        thread.join(10)

    test_case.addCleanup(stop)
    return api


def serve_loopback_api(test_case, api_key: str | None = "mcptestkey"):
    """Point the SDK's module-level settings, which the tools use, at a new
    LoopbackApi for the duration of a test, and give MCP sessions api_key
    as FILES_COM_API_KEY (or none, if api_key is None).

    Each call makes one HTTP attempt, so request counts reflect what the
    tools asked for rather than the retry policy, and a request that gets no
    answer fails after a few seconds instead of the default 80.
    """
    import files_sdk

    api = start_loopback_api(test_case)
    environment = {
        name: value
        for name, value in os.environ.items()
        if name not in ("FILES_COM_API_KEY", "FILES_COM_LOCAL_ROOT")
    }
    if api_key is not None:
        environment["FILES_COM_API_KEY"] = api_key
    patchers: list = [patch.dict(os.environ, environment, clear=True)]
    for name, value in {
        "base_url": api.url,
        "the_api_key": "",
        "max_network_retries": 0,
        "initial_network_retry_delay": 0,
        "max_network_retry_delay": 0,
        "read_timeout": 5,
    }.items():
        patchers.append(patch.object(files_sdk, name, value))
    for patcher in patchers:
        patcher.start()
        test_case.addCleanup(patcher.stop)
    # Close the connections the tools opened before the next test.
    test_case.addCleanup(files_sdk.close)
    return api
