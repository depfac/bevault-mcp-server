"""Projects tools."""

import logging

from fastmcp import FastMCP

from ..client import BeVaultClient

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def get_projects() -> list[dict]:
        """
        Get the list of projects available to the current user.

        Returns only projects the user has explicit read rights on.
        Use the technicalName when calling other tools (e.g. create_hub, create_staging_table).

        Returns:
            A list of dicts with technicalName, displayName, and description for each project.
        """
        try:
            logger.info("get_projects: fetching available projects")
            projects_response = client.projects.get_projects()
            return [
                {
                    "technicalName": p.technicalName or p.name,
                    "displayName": p.displayName,
                    "description": p.description,
                }
                for p in projects_response.projects
            ]
        except Exception:  # noqa: BLE001
            logger.exception("get_projects failed")
            raise
