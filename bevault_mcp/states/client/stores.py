"""Stores client."""

import logging
from typing import Any

from ..models.api import StoresListResponse
from .base import StatesBaseClient

logger = logging.getLogger(__name__)


class StoresClient(StatesBaseClient):
    """Client for store operations."""

    @StatesBaseClient._retry_decorator()
    def list_stores(
        self,
        *,
        page_size: int = 10,
        index: int = 0,
        search_string: str | None = None,
    ) -> StoresListResponse:
        """List stores with optional pagination and name filter."""
        params: dict[str, Any] = {
            "pageSize": page_size,
            "index": index,
            "InternalOnly": False,
        }
        if search_string:
            params["filter"] = search_string
        logger.debug(
            "list_stores: page_size=%s, index=%s, search_string=%s",
            page_size,
            index,
            search_string,
        )
        data = self._get("/api/stores", params=params)
        return StoresListResponse.model_validate(data)
