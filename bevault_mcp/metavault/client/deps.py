"""Process-wide access to the singleton MetaVault client.

FileSystemProvider imports tool modules as standalone files, so tools cannot
receive the client through a closure. They call get_metavault_client() instead.
The client is created once in create_mcp_server() and registered here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MetavaultClient

_client: MetavaultClient | None = None


def init_metavault_client(client: MetavaultClient) -> None:
    """Register the singleton MetaVault client at server startup."""
    global _client
    _client = client


def get_metavault_client() -> MetavaultClient:
    """Return the MetaVault client, or raise if the module is not enabled."""
    if _client is None:
        raise RuntimeError("MetaVault module is not enabled")
    return _client
