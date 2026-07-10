"""State machine entity models."""

import json
from typing import Any

from pydantic import field_validator

from ..base import StatesEntity


def _coerce_default_input(v: object) -> object:
    """Normalize API defaultInput values that may be dict, null, or malformed strings."""
    if not isinstance(v, str):
        return v
    if not v.strip():
        return None
    try:
        parsed = json.loads(v)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    return None


class _StateMachineDefaultInputMixin:
    """Coerce API string defaultInput values to dict or None."""

    @field_validator("defaultInput", mode="before")
    @classmethod
    def coerce_default_input(cls, v: object) -> object:
        return _coerce_default_input(v)


class StateMachineTag(StatesEntity):
    """Tag attached to a state machine."""

    name: str
    value: str


class StateMachine(_StateMachineDefaultInputMixin, StatesEntity):
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


class StateMachineListItem(_StateMachineDefaultInputMixin, StatesEntity):
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
