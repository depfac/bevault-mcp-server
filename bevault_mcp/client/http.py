"""Shared HTTP utilities for API clients."""

import logging
from typing import Any, Dict, Optional, Protocol

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


class AuthHeadersProvider(Protocol):
    def _get_auth_headers(self) -> Dict[str, str]: ...


class HttpClientMixin:
    """Mixin providing HTTP verbs and retry logic."""

    _client: httpx.Client

    def _get_auth_headers(self) -> Dict[str, str]:
        raise NotImplementedError

    def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> dict:
        """GET path with auth; raise for status; return JSON."""
        if params is not None:
            logger.debug("GET %s params=%s", path, params)
        else:
            logger.debug("GET %s", path)
        h = self._get_auth_headers()
        if headers:
            h = {**h, **headers}
        resp = self._client.get(path, params=params, headers=h)
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
    def retry_decorator():
        """Standard retry decorator for API calls."""
        return retry(
            reraise=True,
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
            retry=retry_if_exception_type((httpx.TransportError, httpx.ReadTimeout)),
        )
