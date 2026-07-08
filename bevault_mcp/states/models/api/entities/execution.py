"""Execution entity models."""

from typing import Any

from ..base import StatesEntity
from .state_machine import StateMachine


class ExecutionListItem(StatesEntity):
    """Execution item returned by the list endpoint."""

    stateMachineName: str
    name: str
    status: str
    startDate: str | None = None
    stopDate: str | None = None
    input: Any = None
    output: Any = None
    error: str | None = None
    cause: str | None = None


class Execution(ExecutionListItem):
    """Full execution detail from the States API."""

    stateMachineForExecution: StateMachine | None = None
    self: str | None = None
