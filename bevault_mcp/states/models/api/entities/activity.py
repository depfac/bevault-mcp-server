"""Activity entity models."""

from ..base import StatesEntity


class ActivityTag(StatesEntity):
    """Tag attached to an activity."""

    name: str
    value: str


class ActivityListItem(StatesEntity):
    """Activity item returned by the list endpoint."""

    name: str
    tags: list[ActivityTag] = []
    creationDate: str | None = None
    numberOfWaitingState: int = 0
    averageSuccessTime: float = 0.0
    averageWaitingTime: float = 0.0
    lastContact: str | None = None
    self: str | None = None
