"""Staging tables tools."""

import logging
from typing import Any

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..models import CreateStagingTableRequest, StagingTableColumn
from ..models.api.entities.mapping import HubMapping, LinkMapping, SatelliteMapping
from ..models.api.responses.mappings import ColumnMapping, FormattedMapping
from ..models.requests.staging_table import (
    BaseTypeRequest,
    UpdateStagingTableColumnRequest,
)

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def create_staging_table(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        tableName: str,
        queryType: str,
        query: str | None = None,
        columns: list[dict[str, Any]] | None = None,
    ) -> dict:
        """
        Create a staging table in a data package within a beVault project.

        There are 4 ways to create a staging table:
        1. **Column list**: Provide a structured list of columns with their definitions
        2. **View**: Provide a SELECT statement to create a view
        3. **DDL Table**: Provide DDL column definitions as text
        4. **Existing table**: Reference an existing table in the stg schema (just provide tableName)

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package
            tableName: Name of the staging table (mandatory, must be unique)
            queryType: Type of table - "Table" or "View" (required)
            query: For DDL Table: column definitions as text (e.g., "id text, name text")
                   For View: SELECT statement (e.g., "SELECT * FROM stg.table_name")
                   For Existing table: omit or use empty string
                   For Column list: omit or use empty string
            columns: List of column definitions (only for column list creation). Each column is a dict with:
                   - name (str, required): Column name
                   - dataType (str, required): Column type (DateTime, Date, Text, Boolean, Integer, Numeric, or API types)
                   - length (int, optional): Length for String/Text types (required for Text/String)
                   - businessDescription (str, optional): Business description
                   - businessName (str, optional): Business name
                   - technicalDescription (str, optional): Technical description

        Returns:
            The created staging table entity as a dictionary.
        """
        try:
            logger.info(
                "create_staging_table: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, tableName=%s, queryType=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableName,
                queryType,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Validate queryType
            if queryType not in ["Table", "View"]:
                raise ValueError("queryType must be 'Table' or 'View'")

            # Process columns if provided
            column_list = None
            if columns:
                column_list = []
                for col in columns:
                    if "name" not in col or "dataType" not in col:
                        raise ValueError("Each column must have 'name' and 'dataType'")

                    column_list.append(
                        StagingTableColumn(
                            name=col["name"],
                            dataType=col[
                                "dataType"
                            ],  # Type mapping happens in the model
                            length=col.get("length"),
                            businessDescription=col.get("businessDescription"),
                            businessName=col.get("businessName"),
                            technicalDescription=col.get("technicalDescription"),
                        )
                    )

            # Build the staging table request
            staging_table_request = CreateStagingTableRequest(
                tableName=tableName,
                queryType=queryType,
                query=query or "",
                columns=column_list,
            )

            # Create the staging table
            created_staging_table = client.source_systems.create_staging_table(
                project_id,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                staging_table_request,
            )

            # Return the created staging table as a dictionary
            return created_staging_table.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("create_staging_table failed")
            raise

    @mcp.tool()
    def add_staging_table_column(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        tableIdOrName: str,
        name: str,
        dataType: str,
        baseTypeDataType: str,
        businessDescription: str | None = None,
        hardRuleDefinition: str | None = None,
        length: int | None = None,
        baseTypeLength: int | None = None,
    ) -> dict:
        """
        Add a column to an existing staging table.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package
            tableIdOrName: ID (GUID) or name of the staging table
            name: Column name (required)
            dataType: Target column type. User-friendly types (DateTime, Date, Text, Boolean, Integer, Numeric) are automatically mapped to API types (DateTime2, Date, String, Boolean, Int32, VarNumeric). You can also use API types directly.
            baseTypeDataType: Source type dataType (the original type before any casting). User-friendly types are automatically mapped.
            businessDescription: Business description of the column (optional)
            hardRuleDefinition: Target database specific SQL code for type casting using {{column_name}} syntax (optional). Ex: "{{contract_number}}::int" for PostgreSQL.
            length: Length for String target type (optional, required for String/Text dataType)
            baseTypeLength: Length for String base type (optional, required for String/Text baseTypeDataType)

        Returns:
            The created column entity as a dictionary.
        """
        try:
            logger.info(
                "add_staging_table_column: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, tableIdOrName=%s, name=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableIdOrName,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Create baseType object (simplified - backend will fill in isText, isBinary, autoIncrement)
            base_type = BaseTypeRequest(
                type=baseTypeDataType,
                dataType=baseTypeDataType,  # Type mapping happens in the model
                length=baseTypeLength,
            )

            # Create column request (without id for create)
            column_request = UpdateStagingTableColumnRequest(
                name=name,
                dataType=dataType,  # Type mapping happens in the model
                baseType=base_type,
                businessDescription=businessDescription,
                hardRuleDefinition=hardRuleDefinition,
                length=length,
            )

            # Add the column
            created_column = client.source_systems.add_staging_table_column(
                project_id,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableIdOrName,
                column_request,
            )

            # Return the created column as a dictionary
            return created_column.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("add_staging_table_column failed")
            raise

    @mcp.tool()
    def update_staging_table_column(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        columnId: str,
        name: str,
        dataType: str,
        baseTypeDataType: str,
        businessDescription: str | None = None,
        hardRuleDefinition: str | None = None,
        length: int | None = None,
        baseTypeLength: int | None = None,
    ) -> dict:
        """
        Update a column in a staging table.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package
            columnId: ID (GUID) of the column to update
            name: Column name (required)
            dataType: Target column type. User-friendly types (DateTime, Date, Text, Boolean, Integer, Numeric) are automatically mapped to API types (DateTime2, Date, String, Boolean, Int32, VarNumeric). You can also use API types directly.
            baseTypeDataType: Source type dataType (the original type before any casting). User-friendly types are automatically mapped.
            businessDescription: Business description of the column (optional)
            hardRuleDefinition: Target database specific SQL code for type casting using {{column_name}} syntax (optional). Ex: "{{contract_number}}::int" for PostgreSQL.
            length: Length for String target type (optional, required for String/Text dataType)
            baseTypeLength: Length for String base type (optional, required for String/Text baseTypeDataType)

        Returns:
            The updated column entity as a dictionary.
        """
        try:
            logger.info(
                "update_staging_table_column: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, columnId=%s, name=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                columnId,
                name,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Create baseType object (simplified - backend will fill in isText, isBinary, autoIncrement)
            base_type = BaseTypeRequest(
                type=baseTypeDataType,
                dataType=baseTypeDataType,  # Type mapping happens in the model
                length=baseTypeLength,
            )

            # Create column request (with id for update)
            column_request = UpdateStagingTableColumnRequest(
                id=columnId,
                name=name,
                dataType=dataType,  # Type mapping happens in the model
                baseType=base_type,
                businessDescription=businessDescription,
                hardRuleDefinition=hardRuleDefinition,
                length=length,
            )

            # Update the column
            updated_column = client.source_systems.update_staging_table_column(
                project_id,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                columnId,
                column_request,
            )

            # Return the updated column as a dictionary
            return updated_column.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("update_staging_table_column failed")
            raise

    @mcp.tool()
    def get_staging_table(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        tableIdOrName: str,
    ) -> dict:
        """
        Get information about a staging table including its columns and mappings.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package
            tableId: ID (GUID) of the staging table

        Returns:
            A dictionary containing staging table information with columns and user-friendly mappings.
        """
        try:
            logger.info(
                "get_staging_table: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, tableIdOrName=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Get staging table
            staging_table = client.source_systems.get_staging_table(
                project_id, sourceSystemIdOrName, dataPackageIdOrName, tableIdOrName
            )

            # Get mappings
            mappings_response = client.source_systems.get_staging_table_mappings(
                project_id,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableIdOrName,
                index=0,
                limit=1000000,
            )

            # Create a column lookup by ID
            column_lookup = {col.id: col.name for col in staging_table.columns}

            # Parse all mappings into entity models
            parsed_mappings = {}
            hub_mapping_column_lookup = {}  # mapping_id -> column_name for hub mappings
            link_entities = {}  # link_id -> Link entity (cached to avoid multiple fetches)

            for mapping_data in mappings_response.mappings_list:
                mapping_type = mapping_data.get("mappingType", "")
                mapping_id = mapping_data.get("id")

                if mapping_type == "Hub":
                    mapping = HubMapping.model_validate(mapping_data)
                    parsed_mappings[mapping_id] = mapping
                    column_name = column_lookup.get(
                        mapping.businessKeyMapping.columnId,
                        mapping.businessKeyMapping.columnId,
                    )
                    hub_mapping_column_lookup[mapping_id] = column_name
                elif mapping_type == "Link":
                    mapping = LinkMapping.model_validate(mapping_data)
                    parsed_mappings[mapping_id] = mapping
                    # Fetch Link entity if not already cached
                    if mapping.linkId not in link_entities:
                        try:
                            link_entity = client.model.get_link_by_id(
                                project_id, mapping.linkId
                            )
                            link_entities[mapping.linkId] = link_entity
                        except Exception as e:
                            logger.warning(
                                "Failed to fetch link %s: %s", mapping.linkId, e
                            )
                            link_entities[mapping.linkId] = None
                elif mapping_type == "Satellite":
                    mapping = SatelliteMapping.model_validate(mapping_data)
                    parsed_mappings[mapping_id] = mapping

            # Build formatted mappings with column mappings
            formatted_mappings = []
            for mapping_id, mapping in parsed_mappings.items():
                column_mappings = []

                if isinstance(mapping, HubMapping):
                    # Hub mapping: one column mapping (source column -> business key "bk")
                    source_column_name = hub_mapping_column_lookup.get(mapping_id, "")
                    column_mappings.append(
                        ColumnMapping(
                            sourceColumnName=source_column_name,
                            destinationId=mapping.businessKeyMapping.businessKeyId,
                            destinationType="businessKey",
                            destinationColumnName="bk",
                        )
                    )
                    formatted_mapping = FormattedMapping(
                        id=mapping.id,
                        name=mapping.name,
                        parentName=mapping.parentName,
                        mappingType=mapping.mappingType,
                        columnMappings=column_mappings,
                        isFullLoad=mapping.isFullLoad,
                    )

                elif isinstance(mapping, LinkMapping):
                    # Link mapping: multiple column mappings (hub refs, dependent children, data columns)
                    link_entity = link_entities.get(mapping.linkId)

                    # Build lookups from Link entity's structured fields
                    hub_ref_lookup = {}  # hubReferenceId -> columnName
                    dependent_child_lookup = {}  # dependentChildId -> columnName
                    data_column_lookup = {}  # dataColumnId -> columnName

                    if link_entity:
                        # Hub references
                        for hub_ref in link_entity.hubReferences:
                            hub_ref_lookup[hub_ref.id] = hub_ref.columnName
                        # Dependent children
                        for dep_child in link_entity.dependentChildColumns:
                            dependent_child_lookup[dep_child.id] = dep_child.columnName
                        # Data columns
                        for data_col in link_entity.dataColumns:
                            data_column_lookup[data_col.id] = data_col.columnName

                    # Hub reference column mappings
                    for hub_ref in mapping.hubReferenceColumnMappings:
                        source_column_name = hub_mapping_column_lookup.get(
                            hub_ref.mappingId, ""
                        )
                        destination_column_name = hub_ref_lookup.get(
                            hub_ref.hubReferenceId, ""
                        )
                        column_mappings.append(
                            ColumnMapping(
                                sourceColumnName=source_column_name,
                                destinationId=hub_ref.hubReferenceId,
                                destinationType="hubReference",
                                destinationColumnName=destination_column_name,
                            )
                        )

                    # Dependent child column mappings
                    for dep_child in mapping.dependentChildColumnMappings:
                        source_column_name = column_lookup.get(
                            dep_child.stagingTableColumnId,
                            dep_child.stagingTableColumnId,
                        )
                        destination_column_name = dependent_child_lookup.get(
                            dep_child.dependentChildId, ""
                        )
                        column_mappings.append(
                            ColumnMapping(
                                sourceColumnName=source_column_name,
                                destinationId=dep_child.dependentChildId,
                                destinationType="dependentChild",
                                destinationColumnName=destination_column_name,
                            )
                        )

                    # Data column mappings
                    for data_col in mapping.dataColumnMappings:
                        source_column_name = column_lookup.get(
                            data_col.stagingTableColumnId, data_col.stagingTableColumnId
                        )
                        destination_column_name = data_column_lookup.get(
                            data_col.dataColumnId, ""
                        )
                        column_mappings.append(
                            ColumnMapping(
                                sourceColumnName=source_column_name,
                                destinationId=data_col.dataColumnId,
                                destinationType="dataColumn",
                                destinationColumnName=destination_column_name,
                            )
                        )

                    formatted_mapping = FormattedMapping(
                        id=mapping.id,
                        name=mapping.name,
                        parentName=mapping.parentName,
                        mappingType=mapping.mappingType,
                        columnMappings=column_mappings,
                        isFullLoad=mapping.isFullLoad,
                    )

                elif isinstance(mapping, SatelliteMapping):
                    # Satellite mapping: multiple column mappings (source = destination name)
                    for sat_col in mapping.satelliteColumnMappings:
                        source_column_name = column_lookup.get(
                            sat_col.stagingTableColumnId, sat_col.stagingTableColumnId
                        )
                        column_mappings.append(
                            ColumnMapping(
                                sourceColumnName=source_column_name,
                                destinationId=sat_col.satelliteColumnId,
                                destinationType="satelliteColumn",
                                destinationColumnName=source_column_name,  # Source = destination for satellites
                            )
                        )

                    formatted_mapping = FormattedMapping(
                        id=mapping.id,
                        name=mapping.name,
                        parentName=mapping.parentName,
                        mappingType=mapping.mappingType,
                        columnMappings=column_mappings,
                        isFullLoad=None,  # Satellites don't have isFullLoad
                    )
                else:
                    # Unknown mapping type - include basic info (should not happen)
                    formatted_mapping = FormattedMapping(
                        id=mapping_id,
                        name=getattr(mapping, "name", ""),
                        parentName=getattr(mapping, "parentName", ""),
                        mappingType=getattr(mapping, "mappingType", ""),
                        columnMappings=[],
                        isFullLoad=None,
                    )

                formatted_mappings.append(formatted_mapping)

            # Build the response
            result = {
                "id": staging_table.id,
                "tableName": staging_table.tableName,
                "targetTableName": staging_table.targetTableName,
                "targetSchemaName": staging_table.targetSchemaName,
                "dataPackageId": staging_table.dataPackageId,
                "query": staging_table.query,
                "queryType": staging_table.queryType,
                "isQueryBased": staging_table.isQueryBased,
                "columns": [
                    {
                        "id": col.id,
                        "name": col.name,
                        "dataType": col.dataType,
                        "length": col.length,
                        "scale": col.scale,
                        "precision": col.precision,
                        "nullable": col.nullable,
                        "primaryKey": col.primaryKey,
                        "hardRuleDefinition": col.hardRuleDefinition,
                    }
                    for col in staging_table.columns
                ],
                "mappings": [
                    m.model_dump(mode="json", exclude_none=True)
                    for m in formatted_mappings
                ],
            }

            return result
        except Exception:  # noqa: BLE001
            logger.exception("get_staging_table failed")
            raise

    @mcp.tool()
    def delete_staging_table_column(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        columnId: str,
    ) -> dict:
        """
        Delete a column from a staging table.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package
            columnId: ID (GUID) of the column to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_staging_table_column: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, columnId=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                columnId,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Delete the column
            client.source_systems.delete_staging_table_column(
                project_id, sourceSystemIdOrName, dataPackageIdOrName, columnId
            )

            # Return confirmation
            return {"message": f"Column '{columnId}' deleted successfully"}
        except Exception:  # noqa: BLE001
            logger.exception("delete_staging_table_column failed")
            raise

    @mcp.tool()
    def delete_staging_table(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        tableIdOrName: str,
    ) -> dict:
        """
        Delete a staging table from a data package in a beVault project.

        IMPORTANT: You must first delete all mappings in the staging table before
        deleting it. Use the delete_staging_table_mapping tool to remove each mapping.
        If the staging table has any mappings (Hub, Link, or Satellite), the delete
        operation will fail.

        Args:
            projectName: Technical name of the project (use technicalName from get_projects; will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package
            tableIdOrName: ID (GUID) or name of the staging table to delete

        Returns:
            A confirmation message as a dictionary.
        """
        try:
            logger.info(
                "delete_staging_table: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, tableIdOrName=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug(
                "Found project ID: %s for project: %s", project_id, projectName
            )

            # Delete the staging table
            client.source_systems.delete_staging_table(
                project_id,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableIdOrName,
            )

            return {"message": f"Staging table '{tableIdOrName}' deleted successfully"}
        except Exception:  # noqa: BLE001
            logger.exception("delete_staging_table failed")
            raise
