"""Base client with common HTTP functionality for MetaVault API."""

from typing import Dict

import httpx
from fastmcp.server.dependencies import get_access_token, get_http_headers

from bevault_mcp.config import Settings
from bevault_mcp.shared.http import HttpClientMixin


class BaseClient(HttpClientMixin):
    """Base client with HTTP client and MetaVault authentication."""

    def __init__(self, settings: Settings, http_client: httpx.Client) -> None:
        self._settings = settings
        self._client = http_client

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get headers with Authorization for beVault API calls.

        Uses get_access_token() when OIDC is configured—the auth header is stripped
        by get_http_headers() by default, but the validated token is available
        from the auth context. Falls back to headers (bevault-api-key) when no
        OIDC token is present.
        """
        access_token = get_access_token()
        if access_token is not None and access_token.token:
            return {"Authorization": f"Bearer {access_token.token}"}

        headers = get_http_headers(include={"authorization", "bevault-api-key"})
        auth_header = headers.get("authorization") or headers.get("bevault-api-key")
        if auth_header:
            return {"Authorization": auth_header}
        return {}

    @staticmethod
    def _retry_decorator():
        """Standard retry decorator for API calls."""
        return HttpClientMixin.retry_decorator()
