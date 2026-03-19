"""Base client with common HTTP functionality."""

import logging
from typing import Any, Dict, Optional

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

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """GET path with auth; raise for status; return JSON."""
        if params is not None:
            logger.debug("GET %s params=%s", path, params)
        else:
            logger.debug("GET %s", path)
        resp = self._client.get(path, params=params, headers=self._get_auth_headers())
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, body: dict) -> dict:
        """POST path with body and auth; raise for status; return JSON."""
        logger.debug("POST %s body=%s", path, body)
        resp = self._client.post(path, json=body, headers=self._get_auth_headers())
        resp.raise_for_status()
        return resp.json()

    def _put(self, path: str, body: dict) -> dict:
        """PUT path with body and auth; raise for status; return JSON."""
        logger.debug("PUT %s body=%s", path, body)
        resp = self._client.put(path, json=body, headers=self._get_auth_headers())
        resp.raise_for_status()
        return resp.json()

    def _delete(self, path: str) -> None:
        """DELETE path with auth; raise for status."""
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()

    @staticmethod
    def _retry_decorator():
        """Standard retry decorator for API calls."""
        return retry(
            reraise=True,
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
            retry=retry_if_exception_type((httpx.TransportError, httpx.ReadTimeout)),
        )
