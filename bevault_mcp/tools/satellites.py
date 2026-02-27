"""Satellite tools."""

import logging

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..client.utils import is_guid

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def get_satellite(
        projectName: str,
        parentType: str,
        parentIdOrName: str,
        satelliteIdOrName: str,
    ) -> dict:
        """
        Get satellite details by project name, parent type, parent ID/name, and satellite ID/name.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            parentType: Type of parent - "hub" or "link"
            parentIdOrName: ID (GUID) or name of the parent hub or link
            satelliteIdOrName: ID (GUID) or name of the satellite

        Returns:
            The satellite entity as a dictionary with all details including columns and parent.
        """
        try:
            logger.info(
                "get_satellite: projectName=%s, parentType=%s, parentIdOrName=%s, satelliteIdOrName=%s",
                projectName,
                parentType,
                parentIdOrName,
                satelliteIdOrName,
            )

            # Validate parent type
            if parentType not in ("hub", "link"):
                raise ValueError(
                    f"Invalid parentType '{parentType}'. Must be 'hub' or 'link'"
                )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve parent ID from name if needed
            parent_id = parentIdOrName
            if not is_guid(parentIdOrName):
                if parentType == "hub":
                    parent_entity = client.model.get_hub_by_id(
                        project_id, parentIdOrName
                    )
                else:  # parentType == "link"
                    parent_entity = client.model.get_link_by_id(
                        project_id, parentIdOrName
                    )
                parent_id = parent_entity.id
                logger.debug(
                    "Resolved parent %s name '%s' to ID: %s",
                    parentType,
                    parentIdOrName,
                    parent_id,
                )

            # Get satellite (API may accept name or ID in URL)
            satellite_entity = client.model.get_satellite(
                project_id, parentType, parent_id, satelliteIdOrName
            )

            # Return the satellite entity as a dictionary
            return satellite_entity.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("get_satellite failed")
            raise
