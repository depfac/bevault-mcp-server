"""State machine MCP tool request parameters and API request bodies."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ListStateMachinesParams(BaseModel):
    """Parameters for the list_state_machines MCP tool."""

    searchString: str | None = None
    index: int = 0
    pageSize: int = 10


class GetStateMachineParams(BaseModel):
    """Parameters for the get_state_machine MCP tool."""

    stateMachineName: str


class CreateStateMachineRequest(BaseModel):
    """Request body for POST /api/stateMachines."""

    model_config = ConfigDict(extra="forbid")

    name: str
    definition: dict[str, Any]
    defaultInput: dict[str, Any] | None = None
    isUserFavorite: bool = False


class UpdateStateMachineRequest(BaseModel):
    """Request body for PUT /api/stateMachines/{name}."""

    model_config = ConfigDict(extra="forbid")

    definition: dict[str, Any]
    defaultInput: dict[str, Any] | None = None


class CreateStateMachineParams(BaseModel):
    """Parameters for the create_state_machine MCP tool."""

    stateMachineName: str
    definition: dict[str, Any]
    defaultInput: dict[str, Any] | None = None


class UpdateStateMachineParams(BaseModel):
    """Parameters for the update_state_machine MCP tool."""

    stateMachineName: str
    definition: dict[str, Any]
    defaultInput: dict[str, Any] | None = None
