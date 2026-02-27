import logging

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..models import CreateHubRequest, BusinessKeyRequest

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def create_hub(
        projectName: str,
        name: str,
        ignoreBusinessKeyCase: bool = False,
        businessKeyLength: int = 255,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
    ) -> dict:
        """
        Create a hub in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            name: Name of the hub (mandatory, must be unique)
            ignoreBusinessKeyCase: Whether to ignore case in business key (default: False)
            businessKeyLength: Length of the business key (default: 255)
            technicalDescription: Technical description of the hub (optional)
            businessDescription: Business description of the hub (optional)

        Returns:
            The created hub entity as a dictionary.
        """
        try:
            logger.info("create_hub: projectName=%s, name=%s", projectName, name)

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build the hub request
            hub_request = CreateHubRequest(
                name=name,
                ignoreBusinessKeyCase=ignoreBusinessKeyCase,
                businessKey=BusinessKeyRequest(length=businessKeyLength),
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
            )

            # Create the hub
            created_hub = client.model.create_hub(project_id, hub_request)

            # Return the created hub as a dictionary
            return created_hub.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_hub failed")
            raise

    @mcp.tool()
    def update_hub(
        projectName: str,
        hubIdOrName: str,
        name: str,
        ignoreBusinessKeyCase: bool = False,
        businessKeyLength: int = 255,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
    ) -> dict:
        """
        Update a hub in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            hubIdOrName: ID (GUID) or name of the hub to update
            name: Name of the hub (mandatory, must be unique)
            ignoreBusinessKeyCase: Whether to ignore case in business key (default: False)
            businessKeyLength: Length of the business key (default: 255)
            technicalDescription: Technical description of the hub (optional)
            businessDescription: Business description of the hub (optional)

        Returns:
            The updated hub entity as a dictionary.
        """
        try:
            logger.info(
                "update_hub: projectName=%s, hubIdOrName=%s, name=%s",
                projectName,
                hubIdOrName,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build the hub request
            hub_request = CreateHubRequest(
                name=name,
                ignoreBusinessKeyCase=ignoreBusinessKeyCase,
                businessKey=BusinessKeyRequest(length=businessKeyLength),
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
            )

            # Update the hub
            updated_hub = client.model.update_hub(project_id, hubIdOrName, hub_request)

            # Return the updated hub as a dictionary
            return updated_hub.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_hub failed")
            raise

    @mcp.tool()
    def delete_hub(
        projectName: str,
        hubIdOrName: str,
    ) -> dict:
        """
        Delete a hub from a beVault project.

        IMPORTANT: You must first delete all links referencing the hub before
        deleting it. Use the delete_link tool to remove the links.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            hubIdOrName: ID (GUID) or name of the hub to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_hub: projectName=%s, hubIdOrName=%s", projectName, hubIdOrName
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Delete the hub
            client.model.delete_hub(project_id, hubIdOrName)

            # Return confirmation
            return {"message": f"Hub '{hubIdOrName}' deleted successfully"}
        except Exception:  # noqa: BLE001
            logger.exception("delete_hub failed")
            raise
