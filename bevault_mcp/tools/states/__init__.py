"""States MCP tools registration."""

import logging

from fastmcp import FastMCP

from ...client.states import StatesClient
from .activities import register_fastmcp as register_activities
from .executions import register_fastmcp as register_executions
from .state_machines import register_fastmcp as register_state_machines
from .stores import register_fastmcp as register_stores

logger = logging.getLogger(__name__)


def register_states_tools_fastmcp(mcp: FastMCP, client: StatesClient | None) -> None:
    """Register States module tools with FastMCP instance."""
    if client is None:
        return
    register_state_machines(mcp, client)
    register_executions(mcp, client)
    register_activities(mcp, client)
    register_stores(mcp, client)
    logger.info("States module loaded")
