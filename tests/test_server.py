import unittest

from files_com_mcp import server


class DummyMCP:
    def __init__(self):
        self.http_app_calls = []
        self.run_calls = []

    def http_app(self, **kwargs):
        self.http_app_calls.append(kwargs)
        return {"kind": "http_app", "kwargs": kwargs}

    def run(self, **kwargs):
        self.run_calls.append(kwargs)


class TestServerFactories(unittest.TestCase):
    def test_create_http_app_builds_http_app_from_factory(self):
        dummy_mcp = DummyMCP()

        original_create_mcp = server.create_mcp
        server.create_mcp = lambda: dummy_mcp
        try:
            app = server.create_http_app(path="/")
        finally:
            server.create_mcp = original_create_mcp

        self.assertEqual(app, {"kind": "http_app", "kwargs": {"path": "/"}})
        self.assertEqual(dummy_mcp.http_app_calls, [{"path": "/"}])

    def test_run_stdio_uses_factory_instance(self):
        dummy_mcp = DummyMCP()

        original_create_mcp = server.create_mcp
        server.create_mcp = lambda: dummy_mcp
        try:
            server.run_stdio()
        finally:
            server.create_mcp = original_create_mcp

        self.assertEqual(dummy_mcp.run_calls, [{"transport": "stdio"}])

    def test_run_server_accepts_host_and_port(self):
        dummy_mcp = DummyMCP()

        original_create_mcp = server.create_mcp
        server.create_mcp = lambda: dummy_mcp
        try:
            server.run_server(port=12345, host="0.0.0.0")
        finally:
            server.create_mcp = original_create_mcp

        self.assertEqual(
            dummy_mcp.run_calls,
            [{"transport": "sse", "host": "0.0.0.0", "port": 12345}],
        )


if __name__ == "__main__":
    unittest.main()
