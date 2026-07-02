"""State machine MCP tools."""

import logging
from typing import Any

from fastmcp import FastMCP

from ...client.states import StatesClient
from ...models.states import (
    CreateStateMachineParams,
    CreateStateMachineRequest,
    GetStateMachineParams,
    ListStateMachinesParams,
    UpdateStateMachineParams,
    UpdateStateMachineRequest,
    from_api_list_response,
)

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: StatesClient) -> None:
    @mcp.tool()
    def list_state_machines(
        searchString: str | None = None,
        index: int = 0,
        pageSize: int = 10,
    ) -> dict:
        """
        List state machines in the beVault States module.

        Returns a paginated summary with name, updateDate, and running count only
        (no definition or tags) to keep the response compact.

        Args:
            searchString: Optional filter to search state machines by name.
            index: Page index (0-based).
            pageSize: Number of results per page.

        Returns:
            A dict with paging info and a list of state machine summaries.
        """
        try:
            params = ListStateMachinesParams(
                searchString=searchString,
                index=index,
                pageSize=pageSize,
            )
            logger.info(
                "list_state_machines: searchString=%s, index=%s, pageSize=%s",
                params.searchString,
                params.index,
                params.pageSize,
            )
            api_response = client.state_machines.list_state_machines(
                page_size=params.pageSize,
                index=params.index,
                search_string=params.searchString,
            )
            response = from_api_list_response(api_response)
            return response.model_dump(mode="json")
        except Exception:  # noqa: BLE001
            logger.exception("list_state_machines failed")
            raise

    @mcp.tool()
    def get_state_machine(stateMachineName: str) -> dict:
        """
        Get the full detail of a state machine by name.

        Returns the complete state machine including definition, defaultInput,
        tags, status, and dates. The stateMachineName is case-sensitive and must
        match the exact name returned by list_state_machines.

        Args:
            stateMachineName: Name of the state machine to retrieve.

        Returns:
            The full state machine entity as a dictionary.
        """
        try:
            params = GetStateMachineParams(stateMachineName=stateMachineName)
            logger.info(
                "get_state_machine: stateMachineName=%s", params.stateMachineName
            )
            state_machine = client.state_machines.get_state_machine(
                params.stateMachineName
            )
            return state_machine.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("get_state_machine failed")
            raise

    @mcp.tool()
    def create_state_machine(
        stateMachineName: str,
        definition: dict[str, Any],
        defaultInput: dict[str, Any] | None = None,
    ) -> dict:
        """
        Create a state machine in the beVault States module.

        The definition must be a full Amazon States Language (ASL) JSON object
        using JSONPath only. ASL validation is performed by the States API.
        The stateMachineName must be unique and is case-sensitive.

        Args:
            stateMachineName: Unique name for the new state machine.
            definition: Full ASL definition (StartAt, States, etc.).
            defaultInput: Optional default input passed to executions.

        Returns:
            The created state machine entity as a dictionary.
        """
        try:
            params = CreateStateMachineParams(
                stateMachineName=stateMachineName,
                definition=definition,
                defaultInput=defaultInput,
            )
            logger.info(
                "create_state_machine: stateMachineName=%s",
                params.stateMachineName,
            )
            request = CreateStateMachineRequest(
                name=params.stateMachineName,
                definition=params.definition,
                defaultInput=params.defaultInput,
            )
            state_machine = client.state_machines.create_state_machine(request)
            return state_machine.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_state_machine failed")
            raise

    @mcp.tool()
    def update_state_machine(
        stateMachineName: str,
        definition: dict[str, Any],
        defaultInput: dict[str, Any] | None = None,
    ) -> dict:
        """
        Update an existing state machine in the beVault States module.

        The definition must be a full Amazon States Language (ASL) JSON object
        using JSONPath only. The stateMachineName must match an existing machine
        (case-sensitive). Use get_state_machine first to retrieve the current
        definition before modifying it.

        Args:
            stateMachineName: Name of the state machine to update.
            definition: Full ASL definition (StartAt, States, etc.).
            defaultInput: Optional default input passed to executions.

        Returns:
            The updated state machine entity as a dictionary.
        """
        try:
            params = UpdateStateMachineParams(
                stateMachineName=stateMachineName,
                definition=definition,
                defaultInput=defaultInput,
            )
            logger.info(
                "update_state_machine: stateMachineName=%s",
                params.stateMachineName,
            )
            request = UpdateStateMachineRequest(
                definition=params.definition,
                defaultInput=params.defaultInput,
            )
            state_machine = client.state_machines.update_state_machine(
                params.stateMachineName, request
            )
            return state_machine.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_state_machine failed")
            raise

    @mcp.tool()
    def delete_state_machine(stateMachineName: str) -> dict:
        """
        Delete a state machine from the beVault States module.

        The stateMachineName is case-sensitive and must match an existing machine.
        Ensure no executions are still running before deleting — use
        list_state_machines to check the running count.

        Args:
            stateMachineName: Name of the state machine to delete.

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info("delete_state_machine: stateMachineName=%s", stateMachineName)
            client.state_machines.delete_state_machine(stateMachineName)
            return {
                "message": f"State machine '{stateMachineName}' deleted successfully"
            }
        except Exception:  # noqa: BLE001
            logger.exception("delete_state_machine failed")
            raise
