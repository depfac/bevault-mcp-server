"""State machines client."""

import logging
from typing import Any

from ..models.api import StateMachine, StateMachinesListResponse
from ..models.request import (
    CreateStateMachineRequest,
    UpdateStateMachineRequest,
)
from .base import StatesBaseClient

logger = logging.getLogger(__name__)


class StateMachinesClient(StatesBaseClient):
    """Client for state machine operations."""

    @StatesBaseClient._retry_decorator()
    def list_state_machines(
        self,
        *,
        page_size: int = 10,
        index: int = 0,
        search_string: str | None = None,
    ) -> StateMachinesListResponse:
        """List state machines with optional pagination and name filter."""
        params: dict[str, Any] = {"pageSize": page_size, "index": index}
        if search_string:
            params["filter"] = search_string
        logger.debug(
            "list_state_machines: page_size=%s, index=%s, search_string=%s",
            page_size,
            index,
            search_string,
        )
        data = self._get("/api/stateMachines", params=params)
        return StateMachinesListResponse.model_validate(data)

    @StatesBaseClient._retry_decorator()
    def get_state_machine(self, name: str) -> StateMachine:
        """Get a state machine by name."""
        logger.debug("get_state_machine: name=%s", name)
        data = self._get(f"/api/stateMachines/{name}")
        return StateMachine.model_validate(data)

    @StatesBaseClient._retry_decorator()
    def create_state_machine(self, request: CreateStateMachineRequest) -> StateMachine:
        """Create a state machine."""
        logger.debug("create_state_machine: name=%s", request.name)
        body = request.model_dump(mode="json", exclude_none=True)
        data = self._post("/api/stateMachines", body)
        return StateMachine.model_validate(data)

    @StatesBaseClient._retry_decorator()
    def update_state_machine(
        self, name: str, request: UpdateStateMachineRequest
    ) -> StateMachine:
        """Update a state machine by name."""
        logger.debug("update_state_machine: name=%s", name)
        body = request.model_dump(mode="json", exclude_none=True)
        data = self._put(f"/api/stateMachines/{name}", body)
        return StateMachine.model_validate(data)

    @StatesBaseClient._retry_decorator()
    def delete_state_machine(self, name: str) -> None:
        """Delete a state machine by name."""
        logger.debug("delete_state_machine: name=%s", name)
        self._delete(f"/api/stateMachines/{name}")
