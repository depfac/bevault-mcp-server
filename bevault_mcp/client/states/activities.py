"""Activities client."""

import logging
from typing import Any

from ...models.states.api import ActivitiesListResponse
from .base import StatesBaseClient

logger = logging.getLogger(__name__)


class ActivitiesClient(StatesBaseClient):
    """Client for activity operations."""

    @StatesBaseClient._retry_decorator()
    def list_activities(
        self,
        *,
        page_size: int = 10,
        index: int = 0,
        search_string: str | None = None,
    ) -> ActivitiesListResponse:
        """List activities with optional pagination and name filter."""
        params: dict[str, Any] = {"pageSize": page_size, "index": index}
        if search_string:
            params["filter"] = search_string
        logger.debug(
            "list_activities: page_size=%s, index=%s, search_string=%s",
            page_size,
            index,
            search_string,
        )
        data = self._get("/api/activities", params=params)
        return ActivitiesListResponse.model_validate(data)
