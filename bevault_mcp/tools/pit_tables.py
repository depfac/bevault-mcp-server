"""Pit table tools for beVault MCP."""

import logging

from fastmcp import FastMCP

from ..client import BeVaultClient

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def create_pit_table(
        projectName: str,
        parentType: str,
        parentIdOrName: str,
        snapshotIdOrName: str,
        description: str | None = None,
    ) -> dict:
        """
        Create a pit table for a hub or link in a beVault project.

        Pit tables are Point-in-Time tables that reference a snapshot. All satellites
        of the hub or link are attached automatically by beVault.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects)
            parentType: Type of parent entity - "hub" or "link"
            parentIdOrName: ID (GUID) or name of the hub or link
            snapshotIdOrName: ID (GUID) or name of the snapshot to reference
            description: Optional description for the pit table

        Returns:
            The created pit table entity as a dictionary.
        """
        try:
            logger.info(
                "create_pit_table: projectName=%s, parentType=%s, parentIdOrName=%s, snapshotIdOrName=%s",
                projectName,
                parentType,
                parentIdOrName,
                snapshotIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve snapshot ID from name if needed
            snapshot_id = client.information_marts._resolve_snapshot_id(
                project_id, snapshotIdOrName
            )
            logger.debug(
                "Resolved snapshot ID: %s for: %s", snapshot_id, snapshotIdOrName
            )

            # Validate parent type
            parent_type_lower = parentType.lower()
            if parent_type_lower not in ("hub", "link"):
                raise ValueError(
                    f"Invalid parentType '{parentType}'. Must be 'hub' or 'link'"
                )

            # Create the pit table
            created_pit_table = client.model.create_pit_table(
                project_id=project_id,
                parent_type=parent_type_lower,
                parent_id_or_name=parentIdOrName,
                snapshot_id=snapshot_id,
                description=description,
            )

            return created_pit_table.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_pit_table failed")
            raise

    @mcp.tool()
    def delete_pit_table(
        projectName: str,
        parentType: str,
        parentIdOrName: str,
        pitTableId: str,
    ) -> dict:
        """
        Delete a pit table from a hub or link in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects)
            parentType: Type of parent entity - "hub" or "link"
            parentIdOrName: ID (GUID) or name of the hub or link
            pitTableId: ID (GUID) of the pit table to delete. Use get_hub or get_link
                with includePitTables=True to obtain pit table IDs.

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_pit_table: projectName=%s, parentType=%s, parentIdOrName=%s, pitTableId=%s",
                projectName,
                parentType,
                parentIdOrName,
                pitTableId,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Validate parent type
            parent_type_lower = parentType.lower()
            if parent_type_lower not in ("hub", "link"):
                raise ValueError(
                    f"Invalid parentType '{parentType}'. Must be 'hub' or 'link'"
                )

            # Delete the pit table
            client.model.delete_pit_table(
                project_id=project_id,
                parent_type=parent_type_lower,
                parent_id_or_name=parentIdOrName,
                pit_table_id=pitTableId,
            )

            return {"message": f"Pit table '{pitTableId}' deleted successfully"}
        except Exception:  # noqa: BLE001
            logger.exception("delete_pit_table failed")
            raise
