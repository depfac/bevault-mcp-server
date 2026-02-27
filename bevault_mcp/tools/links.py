import logging
from typing import Any

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..models import (
    CreateLinkRequest,
    DependentChildColumn,
    HubReference,
    LinkType,
)

logger = logging.getLogger(__name__)


def _process_hub_references(
    client: BeVaultClient, project_id: str, hubReferences: list[dict[str, Any]] | None
) -> list[HubReference]:
    """Process hub references, resolving hub names to URLs."""
    hub_refs = []
    if hubReferences:
        for ref in hubReferences:
            if "columnName" not in ref or "hubName" not in ref or "order" not in ref:
                raise ValueError(
                    "Each hubReference must have 'columnName', 'hubName', and 'order'"
                )
            # Get hub by name to get its ID
            hub_name = ref["hubName"]
            hub_entity = client.model.get_hub_by_name(project_id, hub_name)
            # Construct hub URL
            hub_url = client.model.construct_hub_url(project_id, hub_entity.id)
            hub_refs.append(
                HubReference(
                    columnName=ref["columnName"],
                    hub=hub_url,
                    order=ref["order"],
                )
            )
    return hub_refs


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def create_link(
        projectName: str,
        name: str,
        linkType: str = "Relationship",
        dependentChildColumns: list[dict[str, str]] | None = None,
        hubReferences: list[dict[str, Any]] | None = None,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
    ) -> dict:
        """
        Create a link in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            name: Name of the link (mandatory, must be unique)
            linkType: Type of link - Relationship, Hierarchy, Transaction, or SameAs (default: Relationship)
            dependentChildColumns: List of dependent child columns, each with 'columnName' and 'dataType'
            hubReferences: List of hub references, each with 'columnName', 'hubName', and 'order'
                          The hubName will be resolved to a hub URL
            technicalDescription: Technical description of the link (optional)
            businessDescription: Business description of the link (optional)

        Returns:
            The created link entity as a dictionary.
        """
        try:
            logger.info("create_link: projectName=%s, name=%s", projectName, name)

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Parse link type
            try:
                link_type_enum = LinkType(linkType)
            except ValueError:
                raise ValueError(
                    f"Invalid linkType '{linkType}'. Must be one of: Relationship, Hierarchy, Transaction, SameAs"
                )

            # Process dependent child columns
            dependent_columns = []
            if dependentChildColumns:
                for col in dependentChildColumns:
                    if "columnName" not in col or "dataType" not in col:
                        raise ValueError(
                            "Each dependentChildColumn must have 'columnName' and 'dataType'"
                        )
                    dependent_columns.append(
                        DependentChildColumn(
                            columnName=col["columnName"], dataType=col["dataType"]
                        )
                    )

            # Process hub references - resolve hub names to URLs
            hub_refs = _process_hub_references(client, project_id, hubReferences)

            # Build the link request
            link_request = CreateLinkRequest(
                name=name,
                linkType=link_type_enum,
                dependentChildColumns=dependent_columns,
                hubReferences=hub_refs,
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
            )

            # Create the link
            created_link = client.model.create_link(project_id, link_request)

            # Return the created link as a dictionary
            return created_link.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_link failed")
            raise

    @mcp.tool()
    def get_link(
        projectName: str,
        linkIdOrName: str,
    ) -> dict:
        """
        Get link details by project name and link ID or name.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            linkIdOrName: ID (GUID) or name of the link

        Returns:
            The link entity as a dictionary with all details including hub references,
            dependent child columns, and data columns.
        """
        try:
            logger.info(
                "get_link: projectName=%s, linkIdOrName=%s", projectName, linkIdOrName
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )
            link_entity = client.model.get_link_by_id(project_id, linkIdOrName)

            # Return the link entity as a dictionary
            return link_entity.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("get_link failed")
            raise

    @mcp.tool()
    def update_link(
        projectName: str,
        linkIdOrName: str,
        name: str,
        linkType: str = "Relationship",
        dependentChildColumns: list[dict[str, str]] | None = None,
        hubReferences: list[dict[str, Any]] | None = None,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
    ) -> dict:
        """
        Update a link in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            linkIdOrName: ID (GUID) or name of the link to update
            name: Name of the link (mandatory, must be unique)
            linkType: Type of link - Relationship, Hierarchy, Transaction, or SameAs (default: Relationship)
            dependentChildColumns: List of dependent child columns, each with 'columnName' and 'dataType'
            hubReferences: List of hub references, each with 'columnName', 'hubName', and 'order'
                          The hubName will be resolved to a hub URL
            technicalDescription: Technical description of the link (optional)
            businessDescription: Business description of the link (optional)

        Returns:
            The updated link entity as a dictionary.
        """
        try:
            logger.info(
                "update_link: projectName=%s, linkIdOrName=%s, name=%s",
                projectName,
                linkIdOrName,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Parse link type
            try:
                link_type_enum = LinkType(linkType)
            except ValueError:
                raise ValueError(
                    f"Invalid linkType '{linkType}'. Must be one of: Relationship, Hierarchy, Transaction, SameAs"
                )

            # Process dependent child columns
            dependent_columns = []
            if dependentChildColumns:
                for col in dependentChildColumns:
                    if "columnName" not in col or "dataType" not in col:
                        raise ValueError(
                            "Each dependentChildColumn must have 'columnName' and 'dataType'"
                        )
                    dependent_columns.append(
                        DependentChildColumn(
                            columnName=col["columnName"], dataType=col["dataType"]
                        )
                    )

            # Process hub references - resolve hub names to URLs
            hub_refs = _process_hub_references(client, project_id, hubReferences)

            # Build the link request
            link_request = CreateLinkRequest(
                name=name,
                linkType=link_type_enum,
                dependentChildColumns=dependent_columns,
                hubReferences=hub_refs,
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
            )

            # Update the link
            updated_link = client.model.update_link(
                project_id, linkIdOrName, link_request
            )

            # Return the updated link as a dictionary
            return updated_link.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_link failed")
            raise

    @mcp.tool()
    def delete_link(
        projectName: str,
        linkIdOrName: str,
    ) -> dict:
        """
        Delete a link from a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            linkIdOrName: ID (GUID) or name of the link to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_link: projectName=%s, linkIdOrName=%s",
                projectName,
                linkIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Delete the link
            client.model.delete_link(project_id, linkIdOrName)

            # Return confirmation
            return {"message": f"Link '{linkIdOrName}' deleted successfully"}
        except Exception:  # noqa: BLE001
            logger.exception("delete_link failed")
            raise
