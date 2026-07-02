"""Store API response models."""

from ..base import StatesEntity
from ..entities import StoreListItem


class StoresListResponse(StatesEntity):
    """Paginated list of stores from the States API."""

    totalCount: int
    index: int
    pageSize: int | None = None
    results: list[StoreListItem]
    self: str | None = None
