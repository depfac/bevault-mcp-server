"""State machine entity models."""

from typing import Any

from ..base import StatesEntity


class StateMachineTag(StatesEntity):
    """Tag attached to a state machine."""

    name: str
    value: str


class StateMachine(StatesEntity):
    """Full state machine detail from the States API."""

    name: str
    status: str | None = None
    definition: dict[str, Any] | None = None
    defaultInput: dict[str, Any] | None = None
    tags: list[StateMachineTag] = []
    creationDate: str | None = None
    updateDate: str | None = None
    flags: list[str] = []
    self: str | None = None


class StateMachineListItem(StatesEntity):
    """State machine item returned by the list endpoint."""

    name: str
    status: str | None = None
    definition: dict[str, Any] | None = None
    defaultInput: dict[str, Any] | None = None
    tags: list[StateMachineTag] = []
    creationDate: str | None = None
    updateDate: str | None = None
    flags: list[str] = []
    self: str | None = None
    running: int = 0
    isUserFavorite: bool = False
