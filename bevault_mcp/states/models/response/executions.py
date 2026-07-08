"""Optimized execution MCP response models."""

from typing import Any

from pydantic import BaseModel

from ..api import Execution, ExecutionListItem, ExecutionsListResponse
from .state_machines import StatesPagingInfo


class ExecutionSummary(BaseModel):
    """Trimmed execution summary for list responses."""

    stateMachineName: str
    name: str
    status: str
    startDate: str | None = None
    stopDate: str | None = None
    error: str | None = None
    cause: str | None = None


class ListExecutionsResponse(BaseModel):
    """Optimized list_executions MCP tool response."""

    paging: StatesPagingInfo
    executions: list[ExecutionSummary]


def from_api_list_response(
    api_response: ExecutionsListResponse,
) -> ListExecutionsResponse:
    """Convert a States API list response to an optimized MCP response."""
    return ListExecutionsResponse(
        paging=StatesPagingInfo(
            totalCount=api_response.totalCount,
            pageSize=api_response.pageSize,
            index=api_response.index,
        ),
        executions=[_to_summary(item) for item in api_response.results],
    )


def to_get_execution_response(execution: Execution) -> dict[str, Any]:
    """Convert an execution to an MCP response without the state machine definition."""
    data = execution.model_dump(mode="json", exclude_none=True)
    state_machine = data.get("stateMachineForExecution")
    if isinstance(state_machine, dict):
        state_machine.pop("definition", None)
    return data


def to_start_execution_response(execution: Execution) -> dict[str, Any]:
    """Convert an execution to an MCP response without the self URL."""
    return execution.model_dump(mode="json", exclude_none=True, exclude={"self"})


def _to_summary(item: ExecutionListItem) -> ExecutionSummary:
    return ExecutionSummary(
        stateMachineName=item.stateMachineName,
        name=item.name,
        status=item.status,
        startDate=item.startDate,
        stopDate=item.stopDate,
        error=item.error,
        cause=item.cause,
    )
