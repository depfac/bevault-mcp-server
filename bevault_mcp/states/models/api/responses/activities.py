"""Activity API response models."""

from ..base import StatesEntity
from ..entities import ActivityListItem


class ActivitiesListResponse(StatesEntity):
    """Paginated list of activities from the States API."""

    totalCount: int
    pageSize: int
    index: int
    results: list[ActivityListItem]
    self: str | None = None
