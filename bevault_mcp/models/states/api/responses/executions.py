"""Execution API response models."""

from ..base import StatesEntity
from ..entities import ExecutionListItem


class ExecutionsListResponse(StatesEntity):
    """Paginated list of executions from the States API."""

    totalCount: int
    pageSize: int
    index: int
    results: list[ExecutionListItem]
    self: str | None = None
