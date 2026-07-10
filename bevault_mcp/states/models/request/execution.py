"""Execution MCP tool request parameters and API request bodies."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ListExecutionsParams(BaseModel):
    """Parameters for the list_executions MCP tool."""

    stateMachineName: str
    index: int = 0
    pageSize: int = 10


class GetExecutionParams(BaseModel):
    """Parameters for the get_execution MCP tool."""

    stateMachineName: str
    executionName: str


class StartExecutionRequest(BaseModel):
    """Request body for POST /api/stateMachines/{name}/executions."""

    model_config = ConfigDict(extra="forbid")

    input: dict[str, Any]


class StartExecutionParams(BaseModel):
    """Parameters for the start_execution MCP tool."""

    stateMachineName: str
    input: dict[str, Any] | None = None
