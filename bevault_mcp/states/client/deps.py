"""Process-wide access to the singleton States client.

FileSystemProvider imports tool modules as standalone files, so tools cannot
receive the client through a closure. They call get_states_client() instead.
The client is created once in create_mcp_server() and registered here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import StatesClient

_client: StatesClient | None = None


def init_states_client(client: StatesClient) -> None:
    """Register the singleton States client at server startup."""
    global _client
    _client = client


def get_states_client() -> StatesClient:
    """Return the States client, or raise if the module is not enabled."""
    if _client is None:
        raise RuntimeError("States module is not enabled")
    return _client
