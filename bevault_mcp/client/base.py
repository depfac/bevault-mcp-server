"""Base client with common HTTP functionality."""

import logging
from typing import Dict

import httpx
from fastmcp.server.dependencies import get_http_headers
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
        """Get headers with Authorization from HTTP request using FastMCP's get_http_headers()."""
        headers = get_http_headers()
        auth_header = headers.get("authorization") or headers.get("Authorization")
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
