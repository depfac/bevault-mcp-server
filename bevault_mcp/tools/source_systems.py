import logging

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..models import (
    CreateDataPackageRequest,
    CreateSourceSystemRequest,
    OptimizedDataPackage,
    OptimizedSourceSystem,
    OptimizedSourceSystemsResponse,
    PagingInfo,
    StagingTableInfo,
)

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def create_source_system(
        projectName: str,
        name: str,
        code: str,
        version: str | None = None,
        qualityType: int | None = None,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
        dataSteward: str | None = None,
        systemAdministrator: str | None = None,
    ) -> dict:
        """
        Create a source system in a beVault project.

        Args:
            projectName: Name of the project (will be resolved to project ID)
            name: Name of the source system (mandatory, must be unique)
            code: Code of the source system (mandatory)
            version: Version of the source system (optional)
            qualityType: Quality type of the source system (optional, integer)
            technicalDescription: Technical description of the source system (optional)
            businessDescription: Business description of the source system (optional)
            dataSteward: Data steward responsible for the source system (optional)
            systemAdministrator: System administrator for the source system (optional)

        Returns:
            The created source system entity as a dictionary.
        """
        try:
            logger.info(
                "create_source_system: projectName=%s, name=%s", projectName, name
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build the source system request
            source_system_request = CreateSourceSystemRequest(
                name=name,
                code=code,
                version=version,
                qualityType=qualityType,
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
                dataSteward=dataSteward,
                systemAdministrator=systemAdministrator,
            )

            # Create the source system
            created_source_system = client.source_systems.create(
                project_id, source_system_request
            )

            # Return the created source system as a dictionary
            return created_source_system.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_source_system failed")
            raise

    @mcp.tool()
    def create_data_package(
        projectName: str,
        sourceSystemName: str,
        name: str,
        deliverySchedule: str | None = None,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
        refreshType: str | None = None,
        formatInfo: str | None = None,
        expectedQuality: int | None = None,
    ) -> dict:
        """
        Create a data package in a source system within a beVault project.

        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemName: Name or ID of the source system
            name: Name of the data package (mandatory, must be unique)
            deliverySchedule: Delivery schedule of the data package (optional)
            technicalDescription: Technical description of the data package (optional)
            businessDescription: Business description of the data package (optional)
            refreshType: Refresh type of the data package (optional, e.g., "automatic")
            formatInfo: Format information of the data package (optional)
            expectedQuality: Expected quality of the data package (optional, integer)

        Returns:
            The created data package entity as a dictionary.
        """
        try:
            logger.info(
                "create_data_package: projectName=%s, sourceSystemName=%s, name=%s",
                projectName,
                sourceSystemName,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build the data package request
            data_package_request = CreateDataPackageRequest(
                name=name,
                deliverySchedule=deliverySchedule,
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
                refreshType=refreshType,
                formatInfo=formatInfo,
                expectedQuality=expectedQuality,
            )

            # Create the data package
            created_data_package = client.source_systems.create_data_package(
                project_id, sourceSystemName, data_package_request
            )

            # Return the created data package as a dictionary
            return created_data_package.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_data_package failed")
            raise

    @mcp.tool()
    def search_source_systems(
        projectName: str,
        contains: str | None = None,
        index: int = 0,
        limit: int = 10,
    ) -> dict:
        """
        Search source systems in a beVault project.
        Returns optimized paginated response with paging info and source systems (including their data packages).

        Args:
            projectName: Name of the project (will be resolved to project ID)
            contains: Optional filter string - if provided, filters source systems where name contains this value
            index: Pagination index (default: 0)
            limit: Maximum number of results (default: 10)

        Returns:
            Optimized source systems search response with paging and source systems (including packages).
        """
        try:
            logger.info(
                "search_source_systems: projectName=%s, contains=%s",
                projectName,
                contains,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build filter string if contains is provided
            filter_str = None
            if contains:
                filter_str = f"name contains {contains}"

            # Search source systems
            result = client.source_systems.search(
                project_id, index=index, limit=limit, filter=filter_str
            )

            # Transform to optimized format
            optimized_source_systems = []
            for source_system in result.source_systems:
                optimized_packages = []
                for pkg in source_system.packages:
                    # Get staging tables for this data package
                    staging_tables = []
                    try:
                        staging_tables_response = (
                            client.source_systems.get_staging_tables(
                                project_id,
                                source_system.id,
                                pkg.id,
                                index=0,
                                limit=1000000,
                            )
                        )
                        staging_tables = [
                            StagingTableInfo(id=table.id, name=table.tableName)
                            for table in staging_tables_response.tables
                        ]
                        logger.debug(
                            "Found %d staging tables for data package '%s'",
                            len(staging_tables),
                            pkg.name,
                        )
                    except Exception as e:
                        logger.warning(
                            "Failed to fetch staging tables for data package '%s' (id: %s): %s",
                            pkg.name,
                            pkg.id,
                            e,
                        )
                        # Continue with empty list if fetch fails

                    optimized_packages.append(
                        OptimizedDataPackage(
                            id=pkg.id,
                            name=pkg.name,
                            deliverySchedule=pkg.deliverySchedule,
                            technicalDescription=pkg.technicalDescription,
                            businessDescription=pkg.businessDescription,
                            refreshType=pkg.refreshType,
                            formatInfo=pkg.formatInfo,
                            expectedQuality=pkg.expectedQuality,
                            stagingTables=staging_tables,
                        )
                    )

                optimized_source_system = OptimizedSourceSystem(
                    id=source_system.id,
                    name=source_system.name,
                    code=source_system.code,
                    version=source_system.version,
                    qualityType=source_system.qualityType,
                    dataSteward=source_system.dataSteward,
                    systemAdministrator=source_system.systemAdministrator,
                    technicalDescription=source_system.technicalDescription,
                    businessDescription=source_system.businessDescription,
                    packages=optimized_packages,
                )
                optimized_source_systems.append(optimized_source_system)

            # Create optimized response
            optimized_response = OptimizedSourceSystemsResponse(
                paging=PagingInfo(
                    index=result.index,
                    limit=result.limit,
                    total=result.total,
                ),
                sourceSystems=optimized_source_systems,
            )

            return optimized_response.model_dump(mode="json")
        except Exception:  # noqa: BLE001
            logger.exception("search_source_systems failed")
            raise

    @mcp.tool()
    def update_source_system(
        projectName: str,
        sourceSystemIdOrName: str,
        name: str,
        code: str,
        version: str | None = None,
        qualityType: int | None = None,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
        dataSteward: str | None = None,
        systemAdministrator: str | None = None,
    ) -> dict:
        """
        Update a source system in a beVault project.

        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system to update
            name: Name of the source system (mandatory, must be unique)
            code: Code of the source system (mandatory)
            version: Version of the source system (optional)
            qualityType: Quality type of the source system (optional, integer)
            technicalDescription: Technical description of the source system (optional)
            businessDescription: Business description of the source system (optional)
            dataSteward: Data steward responsible for the source system (optional)
            systemAdministrator: System administrator for the source system (optional)

        Returns:
            The updated source system entity as a dictionary.
        """
        try:
            logger.info(
                "update_source_system: projectName=%s, sourceSystemIdOrName=%s, name=%s",
                projectName,
                sourceSystemIdOrName,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build the source system request
            source_system_request = CreateSourceSystemRequest(
                name=name,
                code=code,
                version=version,
                qualityType=qualityType,
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
                dataSteward=dataSteward,
                systemAdministrator=systemAdministrator,
            )

            # Update the source system
            updated_source_system = client.source_systems.update(
                project_id, sourceSystemIdOrName, source_system_request
            )

            # Return the updated source system as a dictionary
            return updated_source_system.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_source_system failed")
            raise

    @mcp.tool()
    def delete_source_system(
        projectName: str,
        sourceSystemIdOrName: str,
    ) -> dict:
        """
        Delete a source system from a beVault project.

        IMPORTANT: You must first delete all data packages in the source system before
        deleting it. Use the delete_data_package tool to remove the data packages.

        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_source_system: projectName=%s, sourceSystemIdOrName=%s",
                projectName,
                sourceSystemIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Delete the source system
            client.source_systems.delete(project_id, sourceSystemIdOrName)

            # Return confirmation
            return {
                "message": f"Source system '{sourceSystemIdOrName}' deleted successfully"
            }
        except Exception:  # noqa: BLE001
            logger.exception("delete_source_system failed")
            raise

    @mcp.tool()
    def update_data_package(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        name: str,
        deliverySchedule: str | None = None,
        technicalDescription: str | None = None,
        businessDescription: str | None = None,
        refreshType: str | None = None,
        formatInfo: str | None = None,
        expectedQuality: int | None = None,
    ) -> dict:
        """
        Update a data package in a source system within a beVault project.

        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package to update
            name: Name of the data package (mandatory, must be unique)
            deliverySchedule: Delivery schedule of the data package (optional)
            technicalDescription: Technical description of the data package (optional)
            businessDescription: Business description of the data package (optional)
            refreshType: Refresh type of the data package (optional, e.g., "automatic")
            formatInfo: Format information of the data package (optional)
            expectedQuality: Expected quality of the data package (optional, integer)

        Returns:
            The updated data package entity as a dictionary.
        """
        try:
            logger.info(
                "update_data_package: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, name=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build the data package request
            data_package_request = CreateDataPackageRequest(
                name=name,
                deliverySchedule=deliverySchedule,
                technicalDescription=technicalDescription,
                businessDescription=businessDescription,
                refreshType=refreshType,
                formatInfo=formatInfo,
                expectedQuality=expectedQuality,
            )

            # Update the data package
            updated_data_package = client.source_systems.update_data_package(
                project_id,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                data_package_request,
            )

            # Return the updated data package as a dictionary
            return updated_data_package.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_data_package failed")
            raise

    @mcp.tool()
    def delete_data_package(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
    ) -> dict:
        """
        Delete a data package from a source system in a beVault project.

        IMPORTANT: You must first delete all staging tables in the data package before
        deleting it. Use the delete_staging_table tool to remove the staging tables.

        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_data_package: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Delete the data package
            client.source_systems.delete_data_package(
                project_id, sourceSystemIdOrName, dataPackageIdOrName
            )

            # Return confirmation
            return {
                "message": f"Data package '{dataPackageIdOrName}' deleted successfully from source system '{sourceSystemIdOrName}'"
            }
        except Exception:  # noqa: BLE001
            logger.exception("delete_data_package failed")
            raise
