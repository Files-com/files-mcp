from . import utils  # noqa: F401

# The release process writes the published version here and in pyproject.toml.
__version__ = "2.0.21"
version = __version__


def create_mcp():
    from .server import create_mcp as _create_mcp

    return _create_mcp()
