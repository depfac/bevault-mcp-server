"""Optimized state machine MCP response models."""

from pydantic import BaseModel

from ..api import StateMachineListItem, StateMachinesListResponse


class StatesPagingInfo(BaseModel):
    """Paging information for States list responses."""

    totalCount: int
    pageSize: int
    index: int


class StateMachineSummary(BaseModel):
    """Trimmed state machine summary for list responses."""

    name: str
    updateDate: str | None = None
    running: int = 0


class ListStateMachinesResponse(BaseModel):
    """Optimized list_state_machines MCP tool response."""

    paging: StatesPagingInfo
    stateMachines: list[StateMachineSummary]


def from_api_list_response(
    api_response: StateMachinesListResponse,
) -> ListStateMachinesResponse:
    """Convert a States API list response to an optimized MCP response."""
    return ListStateMachinesResponse(
        paging=StatesPagingInfo(
            totalCount=api_response.totalCount,
            pageSize=api_response.pageSize,
            index=api_response.index,
        ),
        stateMachines=[_to_summary(item) for item in api_response.results],
    )


def _to_summary(item: StateMachineListItem) -> StateMachineSummary:
    return StateMachineSummary(
        name=item.name,
        updateDate=item.updateDate,
        running=item.running,
    )
