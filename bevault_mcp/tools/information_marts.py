import logging

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..models import (
    CreateInformationMartRequest,
    CreateInformationMartScriptRequest,
    OptimizedInformationMart,
    OptimizedInformationMartScript,
    OptimizedInformationMartsResponse,
    PagingInfo,
    UpdateInformationMartScriptRequest,
    UpdateInformationMartScriptColumnRequest,
    UpdateSourceColumnRequest,
)

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def search_information_marts(
        projectName: str,
        searchName: str | None = None,
        index: int = 0,
        limit: int = 10,
    ) -> dict:
        """
        Search information marts in a beVault project.
        Returns optimized paginated response with paging info and information marts (with simplified script info).

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            searchName: Optional search string - if provided, filters information marts where name contains this value
            index: Pagination index (default: 0)
            limit: Maximum number of results (default: 10)

        Returns:
            Optimized information marts search response with paging and information marts (with simplified scripts).
        """
        try:
            logger.info(
                "search_information_marts: projectName=%s, searchName=%s",
                projectName,
                searchName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Build filter string if searchName is provided
            filter_str = None
            if searchName:
                filter_str = f"name contains {searchName}"

            # Search information marts
            result = client.information_marts.search(
                project_id, index=index, limit=limit, filter=filter_str
            )

            # Transform to optimized format
            optimized_information_marts = []
            for im in result.information_marts:
                # Extract only simplified script info: id, name, order, businessDescription
                optimized_scripts = []
                for script in im.scripts:
                    optimized_scripts.append(
                        OptimizedInformationMartScript(
                            id=script.id,
                            name=script.name,
                            order=script.order,
                            businessDescription=script.businessDescription,
                        )
                    )

                optimized_im = OptimizedInformationMart(
                    id=im.id,
                    name=im.name,
                    businessDescription=im.businessDescription,
                    technicalDescription=im.technicalDescription,
                    schema_=im.schema_,
                    prefix=im.prefix,
                    scriptsCount=im.scriptsCount,
                    snapshotId=im.snapshotId,
                    scripts=optimized_scripts,
                )
                optimized_information_marts.append(optimized_im)

            # Create optimized response
            optimized_response = OptimizedInformationMartsResponse(
                paging=PagingInfo(
                    index=result.index,
                    limit=result.limit,
                    total=result.total,
                ),
                informationMarts=optimized_information_marts,
            )

            return optimized_response.model_dump(mode="json")
        except Exception:  # noqa: BLE001
            logger.exception("search_information_marts failed")
            raise

    @mcp.tool()
    def get_information_mart_script(
        projectName: str,
        informationMartIdOrName: str,
        scriptIdOrName: str,
    ) -> dict:
        """
        Get a full information mart script by ID or name.
        Returns the complete script metadata including columns and their source columns.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            informationMartIdOrName: Information mart ID or name (will be resolved to ID)
            scriptIdOrName: Script ID or name (will be resolved to ID)

        Returns:
            Full information mart script entity with all metadata, columns, and sourceColumns.
        """
        try:
            logger.info(
                "get_information_mart_script: projectName=%s, informationMartIdOrName=%s, scriptIdOrName=%s",
                projectName,
                informationMartIdOrName,
                scriptIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve information mart ID
            information_mart_id = client.information_marts._resolve_information_mart_id(
                project_id, informationMartIdOrName
            )
            logger.debug(
                "Resolved information mart ID: %s for: %s",
                information_mart_id,
                informationMartIdOrName,
            )

            # Resolve script ID
            script_id = client.information_marts._resolve_script_id(
                project_id, information_mart_id, scriptIdOrName
            )
            logger.debug("Resolved script ID: %s for: %s", script_id, scriptIdOrName)

            # Get full script with all metadata
            script = client.information_marts.get_script(
                project_id, information_mart_id, script_id
            )

            # Return the full script as a dictionary
            return script.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("get_information_mart_script failed")
            raise

    @mcp.tool()
    def create_information_mart(
        projectName: str,
        name: str,
        schema: str,
        prefix: str | None = None,
        snapshotIdOrName: str | None = None,
        businessDescription: str | None = None,
        technicalDescription: str | None = None,
    ) -> dict:
        """
        Create an information mart in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            name: Name of the information mart (required)
            schema: Schema name for the information mart (required)
            prefix: Table prefix for the information mart (optional)
            snapshotIdOrName: Snapshot ID or name (optional, will be resolved if provided)
            businessDescription: Business description of the information mart (optional)
            technicalDescription: Technical description of the information mart (optional)

        Returns:
            The created information mart entity as a dictionary.
        """
        try:
            logger.info(
                "create_information_mart: projectName=%s, name=%s, schema=%s, snapshotIdOrName=%s",
                projectName,
                name,
                schema,
                snapshotIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve snapshot ID if provided
            snapshot_id = None
            if snapshotIdOrName:
                snapshot_id = client.information_marts._resolve_snapshot_id(
                    project_id, snapshotIdOrName
                )
                logger.debug(
                    "Resolved snapshot ID: %s for: %s", snapshot_id, snapshotIdOrName
                )

            # Build the information mart request
            information_mart_request = CreateInformationMartRequest(
                name=name,
                databaseSchema=schema,
                prefix=prefix,
                snapshotId=snapshot_id,
                businessDescription=businessDescription,
                technicalDescription=technicalDescription,
            )

            # Create the information mart
            created_im = client.information_marts.create(
                project_id, information_mart_request
            )

            # Return the created information mart as a dictionary
            return created_im.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_information_mart failed")
            raise

    @mcp.tool()
    def create_information_mart_script(
        projectName: str,
        informationMartIdOrName: str,
        name: str,
        order: int | None = None,
        timeout: int = 60,
        tableName: str | None = None,
        businessDescription: str | None = None,
        technicalDescription: str | None = None,
    ) -> dict:
        """
        Create an information mart script in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            informationMartIdOrName: ID (GUID) or name of the information mart
            name: Name of the script (required)
            order: Execution order (optional, will be calculated as max(order) + 1 if not provided)
            timeout: Execution timeout in seconds (default: 60)
            tableName: Table name for the script (optional)
            businessDescription: Business description of the script (optional)
            technicalDescription: Technical description of the script (optional)

        Returns:
            The created information mart script entity as a dictionary.
        """
        try:
            logger.info(
                "create_information_mart_script: projectName=%s, informationMartIdOrName=%s, name=%s, order=%s",
                projectName,
                informationMartIdOrName,
                name,
                order,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve information mart ID
            information_mart_id = client.information_marts._resolve_information_mart_id(
                project_id, informationMartIdOrName
            )
            logger.debug(
                "Resolved information mart ID: %s for: %s",
                information_mart_id,
                informationMartIdOrName,
            )

            # Calculate order if not provided
            script_order = order
            if script_order is None:
                script_order = client.information_marts._calculate_next_order(
                    project_id, information_mart_id
                )
                logger.debug("Calculated order: %s for script '%s'", script_order, name)

            # Build the script request
            script_request = CreateInformationMartScriptRequest(
                name=name,
                order=script_order,
                timeout=timeout,
                tableName=tableName,
                businessDescription=businessDescription,
                technicalDescription=technicalDescription,
            )

            # Create the script
            created_script = client.information_marts.create_script(
                project_id, information_mart_id, script_request
            )

            # Return the created script as a dictionary
            return created_script.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_information_mart_script failed")
            raise

    @mcp.tool()
    def update_information_mart_script(
        projectName: str,
        informationMartIdOrName: str,
        scriptIdOrName: str,
        name: str,
        order: int | None = None,
        timeout: int | None = None,
        tableName: str | None = None,
        typeTag: str | None = None,
        businessDescription: str | None = None,
        technicalDescription: str | None = None,
        columns: list[dict] | None = None,
    ) -> dict:
        """
        Update an information mart script's metadata (excluding code) in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            informationMartIdOrName: ID (GUID) or name of the information mart
            scriptIdOrName: ID (GUID) or name of the script to update
            name: Name of the script (required)
            order: Execution order (optional)
            timeout: Execution timeout in seconds (optional)
            tableName: Table name for the script (optional)
            typeTag: Type tag for the script (optional)
            businessDescription: Business description of the script (optional)
            technicalDescription: Technical description of the script (optional)
            columns: List of column dictionaries (optional). Each dict should contain:
                - name (required)
                - id (optional, if updating existing column)
                - comment (optional)
                - softRule (optional)
                - sourceColumns (optional, list of dicts with source column attributes):
                    - entityType (required): Hub | Link | Satellite | Snapshot | Reference Table | Other
                    - entityName (required): Table name of the entity. It corresponds to the table used in the script's code
                    - columnName (required): Name of the column used in the script's code
                    - id (optional, if updating existing source column)

        Returns:
            The updated information mart script entity as a dictionary.
        """
        try:
            logger.info(
                "update_information_mart_script: projectName=%s, informationMartIdOrName=%s, scriptIdOrName=%s, name=%s",
                projectName,
                informationMartIdOrName,
                scriptIdOrName,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve information mart ID
            information_mart_id = client.information_marts._resolve_information_mart_id(
                project_id, informationMartIdOrName
            )
            logger.debug(
                "Resolved information mart ID: %s for: %s",
                information_mart_id,
                informationMartIdOrName,
            )

            # Resolve script ID
            script_id = client.information_marts._resolve_script_id(
                project_id, information_mart_id, scriptIdOrName
            )
            logger.debug("Resolved script ID: %s for: %s", script_id, scriptIdOrName)

            # Fetch existing script to get current values for fields not provided
            existing_script = client.information_marts.get_script(
                project_id, information_mart_id, script_id
            )

            # Build column request models
            column_requests = []
            if columns:
                # Use provided columns
                for col_dict in columns:
                    source_column_requests = []
                    if "sourceColumns" in col_dict and col_dict["sourceColumns"]:
                        for src_col_dict in col_dict["sourceColumns"]:
                            source_column_requests.append(
                                UpdateSourceColumnRequest(
                                    id=src_col_dict.get("id"),
                                    entityType=src_col_dict["entityType"],
                                    entityName=src_col_dict["entityName"],
                                    columnName=src_col_dict["columnName"],
                                    informationMartId=information_mart_id,
                                    informationMartScriptId=script_id,
                                    informationMartScriptColumnId=col_dict.get("id"),
                                )
                            )

                    column_requests.append(
                        UpdateInformationMartScriptColumnRequest(
                            id=col_dict.get("id"),
                            name=col_dict["name"],
                            informationMartId=information_mart_id,
                            informationMartScriptId=script_id,
                            comment=col_dict.get("comment"),
                            softRule=col_dict.get("softRule"),
                            sourceColumns=source_column_requests,
                        )
                    )
            else:
                # Convert existing columns to request format
                for col in existing_script.columns:
                    source_column_requests = []
                    for src_col in col.sourceColumns:
                        source_column_requests.append(
                            UpdateSourceColumnRequest(
                                id=src_col.id,
                                entityType=src_col.entityType,
                                entityName=src_col.entityName,
                                columnName=src_col.columnName,
                                informationMartId=information_mart_id,
                                informationMartScriptId=script_id,
                                informationMartScriptColumnId=col.id,
                            )
                        )

                    column_requests.append(
                        UpdateInformationMartScriptColumnRequest(
                            id=col.id,
                            name=col.name,
                            informationMartId=information_mart_id,
                            informationMartScriptId=script_id,
                            comment=col.comment,
                            softRule=col.softRule,
                            sourceColumns=source_column_requests,
                        )
                    )

            # Build the script request
            script_request = UpdateInformationMartScriptRequest(
                id=script_id,
                name=name,
                informationMartId=information_mart_id,
                order=order if order is not None else existing_script.order,
                timeout=timeout if timeout is not None else existing_script.timeout,
                tableName=tableName
                if tableName is not None
                else existing_script.tableName,
                typeTag=typeTag if typeTag is not None else existing_script.typeTag,
                businessDescription=businessDescription
                if businessDescription is not None
                else existing_script.businessDescription,
                technicalDescription=technicalDescription
                if technicalDescription is not None
                else existing_script.technicalDescription,
                code=existing_script.code,  # Preserve existing code when updating metadata
                columns=column_requests,
            )

            # Update the script
            updated_script = client.information_marts.update_script(
                project_id, information_mart_id, script_id, script_request
            )

            # Return the updated script as a dictionary
            return updated_script.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_information_mart_script failed")
            raise

    @mcp.tool()
    def update_information_mart_script_code(
        projectName: str,
        informationMartIdOrName: str,
        scriptIdOrName: str,
        code: str,
    ) -> dict:
        """
        Update an information mart script's code only in a beVault project.
        This tool fetches the existing script metadata first, then updates only the code field.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            informationMartIdOrName: ID (GUID) or name of the information mart
            scriptIdOrName: ID (GUID) or name of the script to update
            code: The SQL code to set for the script (required)

        Returns:
            The updated information mart script entity as a dictionary.
        """
        try:
            logger.info(
                "update_information_mart_script_code: projectName=%s, informationMartIdOrName=%s, scriptIdOrName=%s",
                projectName,
                informationMartIdOrName,
                scriptIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve information mart ID
            information_mart_id = client.information_marts._resolve_information_mart_id(
                project_id, informationMartIdOrName
            )
            logger.debug(
                "Resolved information mart ID: %s for: %s",
                information_mart_id,
                informationMartIdOrName,
            )

            # Resolve script ID
            script_id = client.information_marts._resolve_script_id(
                project_id, information_mart_id, scriptIdOrName
            )
            logger.debug("Resolved script ID: %s for: %s", script_id, scriptIdOrName)

            # Update the script code (this will fetch existing script and update code)
            updated_script = client.information_marts.update_script_code(
                project_id, information_mart_id, script_id, code
            )

            # Return the updated script as a dictionary
            return updated_script.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_information_mart_script_code failed")
            raise

    @mcp.tool()
    def update_information_mart(
        projectName: str,
        informationMartIdOrName: str,
        name: str,
        schema: str,
        prefix: str | None = None,
        snapshotIdOrName: str | None = None,
        businessDescription: str | None = None,
        technicalDescription: str | None = None,
    ) -> dict:
        """
        Update an information mart in a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            informationMartIdOrName: ID (GUID) or name of the information mart to update
            name: Name of the information mart (required)
            schema: Schema name for the information mart (required)
            prefix: Table prefix for the information mart (optional)
            snapshotIdOrName: Snapshot ID or name (optional, will be resolved if provided)
            businessDescription: Business description of the information mart (optional)
            technicalDescription: Technical description of the information mart (optional)

        Returns:
            The updated information mart entity as a dictionary.
        """
        try:
            logger.info(
                "update_information_mart: projectName=%s, informationMartIdOrName=%s, name=%s, schema=%s, snapshotIdOrName=%s",
                projectName,
                informationMartIdOrName,
                name,
                schema,
                snapshotIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve snapshot ID if provided
            snapshot_id = None
            if snapshotIdOrName:
                snapshot_id = client.information_marts._resolve_snapshot_id(
                    project_id, snapshotIdOrName
                )
                logger.debug(
                    "Resolved snapshot ID: %s for: %s", snapshot_id, snapshotIdOrName
                )

            # Build the information mart request
            information_mart_request = CreateInformationMartRequest(
                name=name,
                databaseSchema=schema,
                prefix=prefix,
                snapshotId=snapshot_id,
                businessDescription=businessDescription,
                technicalDescription=technicalDescription,
            )

            # Update the information mart
            updated_im = client.information_marts.update(
                project_id, informationMartIdOrName, information_mart_request
            )

            # Return the updated information mart as a dictionary
            return updated_im.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_information_mart failed")
            raise

    @mcp.tool()
    def get_snapshots(
        projectName: str,
        index: int = 0,
        limit: int = 1000000,
    ) -> dict:
        """
        Get snapshots for a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            index: Pagination index (default: 0)
            limit: Maximum number of results (default: 1000000 to get all snapshots)

        Returns:
            Paginated snapshots response with paging info and snapshots list.
        """
        try:
            logger.info(
                "get_snapshots: projectName=%s, index=%s, limit=%s",
                projectName,
                index,
                limit,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Get snapshots
            result = client.information_marts.get_snapshots(
                project_id, index=index, limit=limit
            )

            # Return the snapshots response as a dictionary
            return result.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("get_snapshots failed")
            raise

    @mcp.tool()
    def delete_information_mart(
        projectName: str,
        informationMartIdOrName: str,
    ) -> dict:
        """
        Delete an information mart from a beVault project.

        IMPORTANT: You must first delete all scripts in the information mart before
        deleting it. Use the delete_information_mart_script tool to remove the scripts.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            informationMartIdOrName: ID (GUID) or name of the information mart to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_information_mart: projectName=%s, informationMartIdOrName=%s",
                projectName,
                informationMartIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Delete the information mart
            client.information_marts.delete(project_id, informationMartIdOrName)

            # Return confirmation
            return {
                "message": f"Information mart '{informationMartIdOrName}' deleted successfully"
            }
        except Exception:  # noqa: BLE001
            logger.exception("delete_information_mart failed")
            raise

    @mcp.tool()
    def delete_information_mart_script(
        projectName: str,
        informationMartIdOrName: str,
        scriptIdOrName: str,
    ) -> dict:
        """
        Delete an information mart script from a beVault project.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            informationMartIdOrName: ID (GUID) or name of the information mart
            scriptIdOrName: ID (GUID) or name of the script to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_information_mart_script: projectName=%s, informationMartIdOrName=%s, scriptIdOrName=%s",
                projectName,
                informationMartIdOrName,
                scriptIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Resolve information mart ID
            information_mart_id = client.information_marts._resolve_information_mart_id(
                project_id, informationMartIdOrName
            )
            logger.debug(
                "Resolved information mart ID: %s for: %s",
                information_mart_id,
                informationMartIdOrName,
            )

            # Resolve script ID
            script_id = client.information_marts._resolve_script_id(
                project_id, information_mart_id, scriptIdOrName
            )
            logger.debug("Resolved script ID: %s for: %s", script_id, scriptIdOrName)

            # Delete the script
            client.information_marts.delete_script(
                project_id, information_mart_id, script_id
            )

            # Return confirmation
            return {
                "message": f"Information mart script '{scriptIdOrName}' deleted successfully from information mart '{informationMartIdOrName}'"
            }
        except Exception:  # noqa: BLE001
            logger.exception("delete_information_mart_script failed")
            raise
