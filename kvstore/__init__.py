__version__ = "0.1.0"

from .contract import *
from . import contract


def __getattr__(name):
    """Lazy load client and server modules."""
    if name == "KVClient":
        from kvstore.client import KVClient
        return KVClient
    if name == "create_app":
        from kvstore.server import create_app
        return create_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")