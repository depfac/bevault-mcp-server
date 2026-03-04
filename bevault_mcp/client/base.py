"""Base client with common HTTP functionality."""

import logging
from typing import Dict

import httpx
from fastmcp.server.dependencies import get_access_token, get_http_headers
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ..config import Settings

logger = logging.getLogger(__name__)


class BaseClient:
    """Base client with HTTP client and common functionality."""

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
        # OIDC path: token from auth middleware (request.scope["user"])
        access_token = get_access_token()
        if access_token is not None and access_token.token:
            return {"Authorization": f"Bearer {access_token.token}"}

        # Fallback: bevault-api-key or authorization (when explicitly included)
        headers = get_http_headers(include={"authorization", "bevault-api-key"})
        auth_header = headers.get("authorization") or headers.get("bevault-api-key")
        if auth_header:
            return {"Authorization": auth_header}
        return {}

    @staticmethod
    def _retry_decorator():
        """Standard retry decorator for API calls."""
        return retry(
            reraise=True,
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
            retry=retry_if_exception_type((httpx.TransportError, httpx.ReadTimeout)),
        )
