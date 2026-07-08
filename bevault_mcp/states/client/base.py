"""Base client with OAuth-only authentication for States API."""

from typing import Dict

import httpx
from fastmcp.server.dependencies import get_access_token

from ...config import Settings
from bevault_mcp.shared.http import HttpClientMixin


class StatesBaseClient(HttpClientMixin):
    """Base client for States API — requires OIDC Bearer token, no API key fallback."""

    def __init__(self, settings: Settings, http_client: httpx.Client) -> None:
        self._settings = settings
        self._client = http_client

    def _get_auth_headers(self) -> Dict[str, str]:
        access_token = get_access_token()
        if access_token is not None and access_token.token:
            return {"Authorization": f"Bearer {access_token.token}"}
        raise RuntimeError("States requires OIDC authentication")

    @staticmethod
    def _retry_decorator():
        """Standard retry decorator for API calls."""
        return HttpClientMixin.retry_decorator()
