from . import utils  # noqa: F401

__version__ = "0.1.0"


def create_mcp():
    from .server import create_mcp as _create_mcp

    return _create_mcp()


def create_http_app(**http_app_kwargs):
    from .server import create_http_app as _create_http_app

    return _create_http_app(**http_app_kwargs)
