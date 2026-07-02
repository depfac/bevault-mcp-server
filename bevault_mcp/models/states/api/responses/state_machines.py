"""State machine API response models."""

from ..base import StatesEntity
from ..entities import StateMachineListItem


class StateMachinesListResponse(StatesEntity):
    """Paginated list of state machines from the States API."""

    totalCount: int
    pageSize: int
    index: int
    results: list[StateMachineListItem]
    self: str | None = None
