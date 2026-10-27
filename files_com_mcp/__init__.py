from . import utils  # noqa: F401

__version__ = "1.0.104"


def create_mcp():
    from .server import create_mcp as _create_mcp

    return _create_mcp()
