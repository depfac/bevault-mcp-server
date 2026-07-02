"""Executions client."""

import logging
from typing import Any

from ...models.states.api import Execution, ExecutionsListResponse
from ...models.states.request import StartExecutionRequest
from .base import StatesBaseClient

logger = logging.getLogger(__name__)


class ExecutionsClient(StatesBaseClient):
    """Client for execution operations."""

    @StatesBaseClient._retry_decorator()
    def list_executions(
        self,
        state_machine_name: str,
        *,
        page_size: int = 10,
        index: int = 0,
    ) -> ExecutionsListResponse:
        """List executions for a state machine with optional pagination."""
        params: dict[str, Any] = {"pageSize": page_size, "index": index}
        logger.debug(
            "list_executions: state_machine_name=%s, page_size=%s, index=%s",
            state_machine_name,
            page_size,
            index,
        )
        data = self._get(
            f"/api/stateMachines/{state_machine_name}/executions",
            params=params,
        )
        return ExecutionsListResponse.model_validate(data)

    @StatesBaseClient._retry_decorator()
    def get_execution(self, state_machine_name: str, execution_name: str) -> Execution:
        """Get an execution by state machine and execution name."""
        logger.debug(
            "get_execution: state_machine_name=%s, execution_name=%s",
            state_machine_name,
            execution_name,
        )
        data = self._get(
            f"/api/stateMachines/{state_machine_name}/executions/{execution_name}"
        )
        return Execution.model_validate(data)

    @StatesBaseClient._retry_decorator()
    def start_execution(
        self, state_machine_name: str, request: StartExecutionRequest
    ) -> Execution:
        """Start a new execution for a state machine."""
        logger.debug(
            "start_execution: state_machine_name=%s",
            state_machine_name,
        )
        body = request.model_dump(mode="json", exclude_none=True)
        data = self._post(
            f"/api/stateMachines/{state_machine_name}/executions",
            body,
        )
        return Execution.model_validate(data)
