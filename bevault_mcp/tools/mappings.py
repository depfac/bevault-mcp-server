"""Mappings tools."""
import logging

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..client.utils import is_guid
from ..models.api.entities.mapping import HubMapping, LinkMapping, SatelliteMapping

logger = logging.getLogger(__name__)

# Constants
_MAX_LIMIT = 1000000  # Large limit to fetch all items


def _resolve_staging_table_id(
    client: BeVaultClient,
    project_id: str,
    source_system_id_or_name: str,
    data_package_id_or_name: str,
    staging_table_id_or_name: str,
) -> str:
    """Resolve staging table name to ID if needed."""
    if is_guid(staging_table_id_or_name):
        return staging_table_id_or_name

    staging_tables_response = client.source_systems.get_staging_tables(
        project_id, source_system_id_or_name, data_package_id_or_name, index=0, limit=_MAX_LIMIT
    )

    for table in staging_tables_response.tables:
        if table.tableName == staging_table_id_or_name:
            logger.debug("Resolved staging table name '%s' to ID: %s", staging_table_id_or_name, table.id)
            return table.id

    raise ValueError(
        f"Staging table '{staging_table_id_or_name}' not found in data package '{data_package_id_or_name}'"
    )


def _resolve_source_system_id(
    client: BeVaultClient,
    project_id: str,
    source_system_id_or_name: str,
) -> str:
    """Resolve source system name to ID if needed."""
    if is_guid(source_system_id_or_name):
        return source_system_id_or_name
    source_system = client.source_systems.get_source_system_by_name(project_id, source_system_id_or_name)
    logger.debug("Resolved source system name '%s' to ID: %s", source_system_id_or_name, source_system.id)
    return source_system.id


def _resolve_data_package_id(
    client: BeVaultClient,
    project_id: str,
    source_system_id: str,
    data_package_id_or_name: str,
) -> str:
    """Resolve data package name to ID if needed."""
    if is_guid(data_package_id_or_name):
        return data_package_id_or_name
    data_package = client.source_systems.get_data_package_by_name(
        project_id, source_system_id, data_package_id_or_name
    )
    logger.debug("Resolved data package name '%s' to ID: %s", data_package_id_or_name, data_package.id)
    return data_package.id


def _get_base_url(client: BeVaultClient) -> str:
    """Get the base URL for API calls."""
    return client._settings.bevault_base_url.rstrip("/")


def _build_hub_url(base_url: str, project_id: str, hub_id_or_name: str) -> str:
    """Build hub URL."""
    return f"{base_url}/metavault/api/projects/{project_id}/model/hubs/{hub_id_or_name}"


def _build_data_package_table_url(
    base_url: str,
    project_id: str,
    source_system_id: str,
    data_package_id: str,
    table_id: str,
) -> str:
    """Build data package table URL."""
    return (
        f"{base_url}/metavault/api/projects/{project_id}/metavault/sourcesystems/"
        f"{source_system_id}/datapackages/{data_package_id}/tables/{table_id}"
    )


def _build_data_package_column_url(
    base_url: str,
    project_id: str,
    source_system_id: str,
    data_package_id: str,
    table_id: str,
    column_name_or_id: str,
) -> str:
    """Build data package column URL."""
    return (
        f"{base_url}/metavault/api/projects/{project_id}/metavault/sourcesystems/"
        f"{source_system_id}/datapackages/{data_package_id}/"
        f"tables/{table_id}/columns/{column_name_or_id}"
    )


def _build_id_and_name_lookups(
    items: list, id_attr: str = "id", name_attr: str = "columnName"
) -> tuple[dict, dict]:
    """Build ID and name lookups from a list of items."""
    lookup_by_id = {}
    lookup_by_name = {}
    for item in items:
        lookup_by_id[getattr(item, id_attr)] = item
        name = getattr(item, name_attr, None)
        if name:
            lookup_by_name[name] = item
    return lookup_by_id, lookup_by_name


def _build_hub_mapping_lookups(mappings_response) -> tuple[dict, dict]:
    """Build hub mapping lookups by ID and name."""
    hub_mapping_by_id = {}
    hub_mapping_by_name = {}
    for mapping_data in mappings_response.mappings_list:
        if mapping_data.get("mappingType") == "Hub":
            hub_mapping = HubMapping.model_validate(mapping_data)
            hub_mapping_by_id[hub_mapping.id] = hub_mapping
            hub_mapping_by_name[hub_mapping.name] = hub_mapping
    return hub_mapping_by_id, hub_mapping_by_name


def _build_parent_mapping_lookups(mappings_response) -> tuple[dict, dict, dict, dict]:
    """Build parent mapping (hub and link) lookups by ID and name."""
    hub_mapping_by_id = {}
    hub_mapping_by_name = {}
    link_mapping_by_id = {}
    link_mapping_by_name = {}
    for mapping_data in mappings_response.mappings_list:
        mapping_type = mapping_data.get("mappingType")
        if mapping_type == "Hub":
            hub_mapping = HubMapping.model_validate(mapping_data)
            hub_mapping_by_id[hub_mapping.id] = hub_mapping
            hub_mapping_by_name[hub_mapping.name] = hub_mapping
        elif mapping_type == "Link":
            link_mapping = LinkMapping.model_validate(mapping_data)
            link_mapping_by_id[link_mapping.id] = link_mapping
            link_mapping_by_name[link_mapping.name] = link_mapping
    return hub_mapping_by_id, hub_mapping_by_name, link_mapping_by_id, link_mapping_by_name


def _resolve_parent_mapping_id(
    client: BeVaultClient,
    project_id: str,
    source_system_id: str,
    data_package_id: str,
    table_id: str,
    parent_mapping_id_or_name: str,
    parent_type: str,
) -> str:
    """Resolve parent mapping ID from name if needed."""
    if is_guid(parent_mapping_id_or_name):
        return parent_mapping_id_or_name
    
    if parent_type not in ("hub", "link"):
        raise ValueError(f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'")
    
    # Get staging table mappings to find parent mapping
    mappings_response = client.source_systems.get_staging_table_mappings(
        project_id, source_system_id, data_package_id, table_id, index=0, limit=_MAX_LIMIT
    )
    
    hub_mapping_by_id, hub_mapping_by_name, link_mapping_by_id, link_mapping_by_name = _build_parent_mapping_lookups(mappings_response)
    
    if parent_type == "hub":
        parent_mapping = hub_mapping_by_name.get(parent_mapping_id_or_name)
        if not parent_mapping:
            raise ValueError(f"Hub mapping '{parent_mapping_id_or_name}' not found in staging table mappings")
        logger.debug("Resolved hub mapping name '%s' to ID: %s", parent_mapping_id_or_name, parent_mapping.id)
        return parent_mapping.id
    else:  # parent_type == "link"
        parent_mapping = link_mapping_by_name.get(parent_mapping_id_or_name)
        if not parent_mapping:
            raise ValueError(f"Link mapping '{parent_mapping_id_or_name}' not found in staging table mappings")
        logger.debug("Resolved link mapping name '%s' to ID: %s", parent_mapping_id_or_name, parent_mapping.id)
        return parent_mapping.id


def _resolve_hub_references(
    client: BeVaultClient,
    project_id: str,
    link_id: str,
    hub_references: list[dict[str, str]],
    hub_mapping_by_id: dict,
    hub_mapping_by_name: dict,
    hub_ref_lookup_by_id: dict,
    hub_ref_lookup_by_name: dict,
    link_name: str,
) -> list[dict]:
    """Resolve hub references details."""
    base_url = _get_base_url(client)
    hub_references_details = []

    for hub_ref_input in hub_references:
        if "hubMappingIdOrName" not in hub_ref_input or "hubReferenceNameOrId" not in hub_ref_input:
            raise ValueError("Each hub reference must have 'hubMappingIdOrName' and 'hubReferenceNameOrId'")

        hub_mapping_id_or_name = hub_ref_input["hubMappingIdOrName"]
        hub_reference_name_or_id = hub_ref_input["hubReferenceNameOrId"]

        # Resolve hub mapping
        hub_mapping = (
            hub_mapping_by_id.get(hub_mapping_id_or_name)
            if is_guid(hub_mapping_id_or_name)
            else hub_mapping_by_name.get(hub_mapping_id_or_name)
        )
        if not hub_mapping:
            raise ValueError(f"Hub mapping '{hub_mapping_id_or_name}' not found in staging table mappings")

        # Resolve hub reference
        hub_reference = (
            hub_ref_lookup_by_id.get(hub_reference_name_or_id)
            if is_guid(hub_reference_name_or_id)
            else hub_ref_lookup_by_name.get(hub_reference_name_or_id)
        )
        if not hub_reference:
            raise ValueError(f"Hub reference '{hub_reference_name_or_id}' not found in link '{link_name}'")

        # Construct URLs
        hub_mapping_url = f"{base_url}/metavault/api/projects/{project_id}/mappings/hubs/{hub_mapping.id}"
        hub_reference_url = (
            f"{base_url}/metavault/api/projects/{project_id}/model/links/{link_id}/"
            f"hubreferences/{hub_reference.id}"
        )

        hub_references_details.append({
            "hubMapping": hub_mapping_url,
            "hubReference": hub_reference_url,
        })

    return hub_references_details


def _resolve_link_column_mappings(
    client: BeVaultClient,
    project_id: str,
    source_system_id: str,
    data_package_id: str,
    table_id: str,
    link_column_inputs: list[dict[str, str]],
    lookup_by_id: dict,
    lookup_by_name: dict,
    link_name: str,
    column_type: str,  # "dependentChild" or "dataColumn"
) -> list[dict]:
    """Resolve link column mappings (dependent children or data columns)."""
    if not link_column_inputs:
        return []

    base_url = _get_base_url(client)
    mappings = []

    for col_input in link_column_inputs:
        if "linkColumnNameOrId" not in col_input or "stagingColumnNameOrId" not in col_input:
            raise ValueError(f"Each {column_type} must have 'linkColumnNameOrId' and 'stagingColumnNameOrId'")

        link_column_name_or_id = col_input["linkColumnNameOrId"]
        staging_column_name_or_id = col_input["stagingColumnNameOrId"]

        # Resolve link column
        link_column = (
            lookup_by_id.get(link_column_name_or_id)
            if is_guid(link_column_name_or_id)
            else lookup_by_name.get(link_column_name_or_id)
        )

        if not link_column:
            raise ValueError(
                f"{column_type.capitalize()} column '{link_column_name_or_id}' not found in link '{link_name}'"
            )

        # Construct staging column URL
        staging_column_url = _build_data_package_column_url(
            base_url,
            project_id,
            source_system_id,
            data_package_id,
            table_id,
            staging_column_name_or_id,
        )

        mappings.append({
            "linkColumnId": link_column.id,
            "dataPackageTableColumn": staging_column_url,
        })

    return mappings


def _resolve_satellite_columns(
    client: BeVaultClient,
    project_id: str,
    source_system_id: str,
    data_package_id: str,
    table_id: str,
    column_names: list[str],
) -> list[str]:
    """Build column URLs from column names."""
    if not column_names:
        return []
    
    base_url = _get_base_url(client)
    column_urls = []
    
    for column_name in column_names:
        column_url = _build_data_package_column_url(
            base_url, project_id, source_system_id, data_package_id, table_id, column_name
        )
        column_urls.append(column_url)
    
    return column_urls


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def map_column_to_hub(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        stagingTableIdOrName: str,
        columnNameOrId: str,
        hubIdOrName: str,
        isFullLoad: bool = False,
        expectNullBusinessKey: bool = False,
    ) -> dict:
        """
        Map a staging table column to a hub.
        
        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system (API accepts both)
            dataPackageIdOrName: ID (GUID) or name of the data package (API accepts both)
            stagingTableIdOrName: ID (GUID) or name of the staging table (will be resolved to ID if not GUID)
            columnNameOrId: Name or ID (GUID) of the column (API accepts both)
            hubIdOrName: ID (GUID) or name of the hub (API accepts both)
            isFullLoad: Whether this is a full load. The staging table contains the complete set of business keys (hub) 
                       for each load. beVault uses this to detect removals (missing keys) and updates effectivity 
                       satellites to track presence over time per source. (default: False)
            expectNullBusinessKey: Define whether the business key can be null or not on a business point of view in 
                                  this staging table. It defines which ghost record will be used when a NULL value 
                                  is detected. (default: False)
        
        Returns:
            The created hub mapping entity as a dictionary
        """
        try:
            logger.info(
                "map_column_to_hub: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, "
                "stagingTableIdOrName=%s, columnNameOrId=%s, hubIdOrName=%s, isFullLoad=%s, expectNullBusinessKey=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                stagingTableIdOrName,
                columnNameOrId,
                hubIdOrName,
                isFullLoad,
                expectNullBusinessKey,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug("Found project ID: %s for project: %s", project_id, projectName)

            # Resolve source system and data package IDs
            source_system_id = _resolve_source_system_id(client, project_id, sourceSystemIdOrName)
            data_package_id = _resolve_data_package_id(client, project_id, source_system_id, dataPackageIdOrName)

            # Resolve staging table ID if needed
            table_id = _resolve_staging_table_id(
                client, project_id, source_system_id, data_package_id, stagingTableIdOrName
            )

            # Construct URLs (no need to resolve column - API accepts both ID and name)
            base_url = _get_base_url(client)
            hub_url = _build_hub_url(base_url, project_id, hubIdOrName)
            data_package_table_url = _build_data_package_table_url(
                base_url, project_id, source_system_id, data_package_id, table_id
            )
            data_package_column_url = _build_data_package_column_url(
                base_url, project_id, source_system_id, data_package_id, table_id, columnNameOrId
            )

            logger.debug(
                "Constructed URLs - hub: %s, table: %s, column: %s",
                hub_url,
                data_package_table_url,
                data_package_column_url,
            )

            # Create the hub mapping
            hub_mapping = client.mappings.create_hub_mapping(
                project_id=project_id,
                hub_url=hub_url,
                data_package_table_url=data_package_table_url,
                data_package_column_url=data_package_column_url,
                is_full_load=isFullLoad,
                expect_null_business_key=expectNullBusinessKey,
            )

            # Return the created hub mapping as a dictionary 
            return hub_mapping.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("map_column_to_hub failed")
            raise

    @mcp.tool()
    def map_columns_to_link(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        stagingTableIdOrName: str,
        linkIdOrName: str,
        hubReferences: list[dict[str, str]],
        dependentChildren: list[dict[str, str]] | None = None,
        dataColumns: list[dict[str, str]] | None = None,
        isFullLoad: bool = True,
    ) -> dict:
        """
        Map staging table columns to a link.
        
        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system (API accepts both)
            dataPackageIdOrName: ID (GUID) or name of the data package (API accepts both)
            stagingTableIdOrName: ID (GUID) or name of the staging table (will be resolved to ID if not GUID)
            linkIdOrName: ID (GUID) or name of the link (API accepts both)
            hubReferences: List of objects with 'hubMappingIdOrName' and 'hubReferenceNameOrId' (mandatory).
                          All hub references from the link must be mapped.
            dependentChildren: List of objects with 'linkColumnNameOrId' and 'stagingColumnNameOrId' (optional).
                             All dependent children from the link must be mapped if provided.
            dataColumns: List of objects with 'linkColumnNameOrId' and 'stagingColumnNameOrId' (optional).
                        All data columns from the link must be mapped if provided.
            isFullLoad: Whether this is a full load. The staging table contains the complete set of 
                       relationships (link) for each load. beVault uses this to detect removals (missing 
                       relationships) and updates effectivity satellites to track presence over time per source. 
                       (default: True)
        
        Returns:
            The created link mapping entity as a dictionary (excluding _links).

        Warning: 
            All hub references, dependent children, and data columns of the link must be mapped.
            You need to map the hubs first, and then the link.
        """
        try:
            logger.info(
                "map_columns_to_link: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, "
                "stagingTableIdOrName=%s, linkIdOrName=%s, isFullLoad=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                stagingTableIdOrName,
                linkIdOrName,
                isFullLoad,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug("Found project ID: %s for project: %s", project_id, projectName)

            # Resolve source system and data package IDs
            source_system_id = _resolve_source_system_id(client, project_id, sourceSystemIdOrName)
            data_package_id = _resolve_data_package_id(client, project_id, source_system_id, dataPackageIdOrName)

            # Resolve staging table ID if needed
            table_id = _resolve_staging_table_id(
                client, project_id, source_system_id, data_package_id, stagingTableIdOrName
            )

            # Get link entity to access embedded hub references, dependent children, and data columns
            link_entity = client.model.get_link_by_id(project_id, linkIdOrName)
            link_id = link_entity.id
            logger.debug("Found link ID: %s for link: %s", link_id, linkIdOrName)

            # Get staging table mappings to find hub mappings
            mappings_response = client.source_systems.get_staging_table_mappings(
                project_id, source_system_id, data_package_id, table_id, index=0, limit=_MAX_LIMIT
            )

            # Build hub mapping lookups
            hub_mapping_by_id, hub_mapping_by_name = _build_hub_mapping_lookups(mappings_response)

            # Build lookups from link entity's structured data
            hub_ref_lookup_by_id, hub_ref_lookup_by_name = _build_id_and_name_lookups(
                link_entity.hubReferences
            )
            dependent_child_lookup_by_id, dependent_child_lookup_by_name = _build_id_and_name_lookups(
                link_entity.dependentChildColumns
            )
            data_column_lookup_by_id, data_column_lookup_by_name = _build_id_and_name_lookups(
                link_entity.dataColumns
            )

            # Resolve hub references details
            hub_references_details = _resolve_hub_references(
                client,
                project_id,
                link_id,
                hubReferences,
                hub_mapping_by_id,
                hub_mapping_by_name,
                hub_ref_lookup_by_id,
                hub_ref_lookup_by_name,
                linkIdOrName,
            )

            # Resolve dependent children
            link_mapping_dependent_child_columns = _resolve_link_column_mappings(
                client,
                project_id,
                source_system_id,
                data_package_id,
                table_id,
                dependentChildren or [],
                dependent_child_lookup_by_id,
                dependent_child_lookup_by_name,
                linkIdOrName,
                "dependentChild",
            )

            # Resolve data columns
            link_mapping_data_columns = _resolve_link_column_mappings(
                client,
                project_id,
                source_system_id,
                data_package_id,
                table_id,
                dataColumns or [],
                data_column_lookup_by_id,
                data_column_lookup_by_name,
                linkIdOrName,
                "dataColumn",
            )

            # Construct link URL and data package table URL
            base_url = _get_base_url(client)
            link_url = f"{base_url}/metavault/api/projects/{project_id}/model/links/{link_id}"
            data_package_table_url = _build_data_package_table_url(
                base_url, project_id, source_system_id, data_package_id, table_id
            )

            logger.debug(
                "Constructed URLs - link: %s, table: %s, hub references: %d, dependent children: %d, data columns: %d",
                link_url,
                data_package_table_url,
                len(hub_references_details),
                len(link_mapping_dependent_child_columns),
                len(link_mapping_data_columns),
            )

            # Create the link mapping
            link_mapping = client.mappings.create_link_mapping(
                project_id=project_id,
                link_url=link_url,
                data_package_table_url=data_package_table_url,
                is_full_load=isFullLoad,
                hub_references_details=hub_references_details if hub_references_details else None,
                link_mapping_dependent_child_columns=link_mapping_dependent_child_columns if link_mapping_dependent_child_columns else None,
                link_mapping_data_columns=link_mapping_data_columns if link_mapping_data_columns else None,
            )

            # Return the created link mapping as a dictionary (excluding _links)
            return link_mapping.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("map_columns_to_link failed")
            raise

    @mcp.tool()
    def map_columns_to_satellite(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        stagingTableIdOrName: str,
        satelliteName: str,
        columnNames: list[str],
        parentMappingId: str,
        parentType: str,
        isMultiActive: bool = False,
        subSequenceColumn: str | None = None,
    ) -> dict:
        """
        Map staging table columns to a satellite.
        
        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system (API accepts both)
            dataPackageIdOrName: ID (GUID) or name of the data package (API accepts both)
            stagingTableIdOrName: ID (GUID) or name of the staging table (will be resolved to ID if not GUID)
            satelliteName: Name of the satellite. It will be prefixed with its parent name, no need to include it.
            columnNames: List of column names that should be included in the satellite
            parentMappingId: ID (GUID) or name of the mapping to which the satellite should be attached to
            parentType: Type of parent mapping - either "hub" or "link"
            isMultiActive: Whether the satellite is multi-active (default: False). Unless explicitly asked by the user, 
                          create descriptive satellite by leaving isMultiActive to false.
            subSequenceColumn: Optional column name. When a satellite is multi-active, this field is used to decide if 
                             the multi-active satellite is delta-driven or not. If the field is filled in with the name 
                             of a column, it will be a delta-driven one and the column chosen will be used to order the 
                             descriptive rows of the same business key to compute a unique hash. Otherwise, it will be a 
                             standard multi-active satellite and all the records will be inserted every load.
        
        Returns:
            The created satellite mapping entity as a dictionary.
        """
        try:
            logger.info(
                "map_columns_to_satellite: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, "
                "stagingTableIdOrName=%s, satelliteName=%s, parentMappingId=%s, parentType=%s, isMultiActive=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                stagingTableIdOrName,
                satelliteName,
                parentMappingId,
                parentType,
                isMultiActive,
            )

            # Validate parent type
            if parentType not in ("hub", "link"):
                raise ValueError(f"Invalid parentType '{parentType}'. Must be 'hub' or 'link'")

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug("Found project ID: %s for project: %s", project_id, projectName)

            # Resolve source system and data package IDs
            source_system_id = _resolve_source_system_id(client, project_id, sourceSystemIdOrName)
            data_package_id = _resolve_data_package_id(client, project_id, source_system_id, dataPackageIdOrName)

            # Resolve staging table ID if needed
            table_id = _resolve_staging_table_id(
                client, project_id, source_system_id, data_package_id, stagingTableIdOrName
            )

            # Resolve parent mapping ID if needed
            parent_mapping_id = _resolve_parent_mapping_id(
                client, project_id, source_system_id, data_package_id, table_id, parentMappingId, parentType
            )

            # Resolve column names to column URLs
            satellite_column_urls = _resolve_satellite_columns(
                client, project_id, source_system_id, data_package_id, table_id, columnNames
            )

            # Build staging table URL
            base_url = _get_base_url(client)
            staging_table_url = _build_data_package_table_url(
                base_url, project_id, source_system_id, data_package_id, table_id
            )

            # Build subSequenceColumn URL if provided
            sub_sequence_column_url = None
            if subSequenceColumn:
                sub_sequence_column_url = _build_data_package_column_url(
                    base_url, project_id, source_system_id, data_package_id, table_id, subSequenceColumn
                )

            logger.debug(
                "Constructed URLs - staging table: %s, columns: %d, subSequenceColumn: %s",
                staging_table_url,
                len(satellite_column_urls),
                sub_sequence_column_url,
            )

            # Create the satellite mapping
            satellite_mapping = client.mappings.create_satellite_mapping(
                project_id=project_id,
                parent_mapping_id=parent_mapping_id,
                parent_type=parentType,
                satellite_name=satelliteName,
                satellite_columns=satellite_column_urls,
                staging_table_url=staging_table_url,
                is_multi_active=isMultiActive,
                sub_sequence_column_url=sub_sequence_column_url,
            )

            # Return the created satellite mapping as a dictionary
            return satellite_mapping.model_dump(mode="json", exclude_none=True)
        except Exception:  # noqa: BLE001
            logger.exception("map_columns_to_satellite failed")
            raise

    @mcp.tool()
    def delete_staging_table_mapping(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        tableIdOrName: str,
        mappingIdOrName: str,
    ) -> dict:
        """
        Delete a mapping from a staging table.
        
        The mapping type (Hub, Link, or Satellite) is automatically determined.
        For satellite mappings, the parent mapping is found to determine the correct delete path.
        
        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system
            dataPackageIdOrName: ID (GUID) or name of the data package
            tableIdOrName: ID (GUID) or name of the staging table
            mappingIdOrName: ID (GUID) or name of the mapping to delete (Ex: A, B, C, etc.)
        
        Returns:
            A confirmation message as a dictionary.
        Usage: 
            You might need to get the information about the staging table first to know the mapping IDs.
        """
        try:
            logger.info(
                "delete_staging_table_mapping: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, tableIdOrName=%s, mappingIdOrName=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                tableIdOrName,
                mappingIdOrName,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug("Found project ID: %s for project: %s", project_id, projectName)

            # Resolve source system ID if needed
            if is_guid(sourceSystemIdOrName):
                source_system_id = sourceSystemIdOrName
            else:
                source_system = client.source_systems.get_source_system_by_name(project_id, sourceSystemIdOrName)
                source_system_id = source_system.id
                logger.debug("Resolved source system name '%s' to ID: %s", sourceSystemIdOrName, source_system_id)

            # Resolve data package ID if needed
            if is_guid(dataPackageIdOrName):
                data_package_id = dataPackageIdOrName
            else:
                data_package = client.source_systems.get_data_package_by_name(
                    project_id, source_system_id, dataPackageIdOrName
                )
                data_package_id = data_package.id
                logger.debug("Resolved data package name '%s' to ID: %s", dataPackageIdOrName, data_package_id)

            # Resolve staging table ID if needed
            if is_guid(tableIdOrName):
                table_id = tableIdOrName
            else:
                staging_tables_response = client.source_systems.get_staging_tables(
                    project_id, source_system_id, data_package_id, index=0, limit=_MAX_LIMIT
                )
                table_id = None
                for table in staging_tables_response.tables:
                    if table.tableName == tableIdOrName:
                        table_id = table.id
                        break
                if not table_id:
                    raise ValueError(
                        f"Staging table '{tableIdOrName}' not found in data package '{dataPackageIdOrName}'"
                    )
                logger.debug("Resolved staging table name '%s' to ID: %s", tableIdOrName, table_id)

            # Get all mappings for the staging table
            mappings_response = client.source_systems.get_staging_table_mappings(
                project_id, source_system_id, data_package_id, table_id, index=0, limit=_MAX_LIMIT
            )

            # Find the mapping by ID or name
            target_mapping = None
            target_mapping_id = None
            for mapping_data in mappings_response.mappings_list:
                mapping_id = mapping_data.get("id")
                mapping_name = mapping_data.get("name", "")
                
                if mapping_id == mappingIdOrName or mapping_name == mappingIdOrName:
                    target_mapping = mapping_data
                    target_mapping_id = mapping_id
                    break

            if not target_mapping:
                raise ValueError(f"Mapping '{mappingIdOrName}' not found in staging table mappings")

            # Determine mapping type and construct delete path
            mapping_type = target_mapping.get("mappingType", "")
            
            if mapping_type == "Hub":
                # Hub mapping: /mappings/hubs/{mappingId}
                delete_path = f"/metavault/api/projects/{project_id}/mappings/hubs/{target_mapping_id}"
                
            elif mapping_type == "Link":
                # Link mapping: /mappings/links/{mappingId}
                delete_path = f"/metavault/api/projects/{project_id}/mappings/links/{target_mapping_id}"
                
            elif mapping_type == "Satellite":
                # Satellite mapping: need to find parent mapping to determine if it's attached to hub or link
                satellite_mapping = SatelliteMapping.model_validate(target_mapping)
                parent_mapping_id = satellite_mapping.satelliteParentMappingId
                
                # Find parent mapping to determine its type
                parent_mapping = None
                for mapping_data in mappings_response.mappings_list:
                    if mapping_data.get("id") == parent_mapping_id:
                        parent_mapping = mapping_data
                        break
                
                if not parent_mapping:
                    raise ValueError(f"Parent mapping '{parent_mapping_id}' not found for satellite mapping")
                
                parent_mapping_type = parent_mapping.get("mappingType", "")
                
                if parent_mapping_type == "Hub":
                    # Satellite attached to hub: /mappings/hubs/{hubId}/satellites/{mappingId}
                    hub_mapping = HubMapping.model_validate(parent_mapping)
                    delete_path = f"/metavault/api/projects/{project_id}/mappings/hubs/{hub_mapping.hubId}/satellites/{target_mapping_id}"
                elif parent_mapping_type == "Link":
                    # Satellite attached to link: /mappings/links/{linkId}/satellites/{mappingId}
                    link_mapping = LinkMapping.model_validate(parent_mapping)
                    delete_path = f"/metavault/api/projects/{project_id}/mappings/links/{link_mapping.linkId}/satellites/{target_mapping_id}"
                else:
                    raise ValueError(f"Invalid parent mapping type '{parent_mapping_type}' for satellite mapping")
            else:
                raise ValueError(f"Unknown mapping type '{mapping_type}'")

            logger.debug("Delete path: %s", delete_path)

            # Delete the mapping
            client.mappings.delete_mapping(project_id, delete_path)

            # Return confirmation
            return {"message": f"Mapping '{mappingIdOrName}' ({mapping_type}) deleted successfully"}
        except Exception as exc:  # noqa: BLE001
            logger.exception("delete_staging_table_mapping failed")
            raise

    @mcp.tool()
    def update_staging_table_satellite_mapping(
        projectName: str,
        sourceSystemIdOrName: str,
        dataPackageIdOrName: str,
        stagingTableIdOrName: str,
        satelliteMappingIdOrName: str,
        satelliteName: str,
        columnNames: list[str],
        isMultiActive: bool = False,
        subSequenceColumn: str | None = None,
    ) -> dict:
        """
        Update a satellite mapping for a staging table.
        
        The parent mapping (hub or link) is automatically determined from the satellite mapping.
        
        Args:
            projectName: Name of the project (will be resolved to project ID)
            sourceSystemIdOrName: ID (GUID) or name of the source system (API accepts both)
            dataPackageIdOrName: ID (GUID) or name of the data package (API accepts both)
            stagingTableIdOrName: ID (GUID) or name of the staging table (will be resolved to ID if not GUID)
            satelliteMappingIdOrName: ID (GUID) or name of the satellite mapping to update. Use the ID if available.
            satelliteName: Name of the satellite. It will be prefixed with its parent name, no need to include it.
            columnNames: List of column names that should be included in the satellite
            isMultiActive: Whether the satellite is multi-active (default: False). Unless explicitly asked by the user, 
                          create descriptive satellite by leaving isMultiActive to false.
            subSequenceColumn: Optional column name. When a satellite is multi-active, this field is used to decide if 
                             the multi-active satellite is delta-driven or not. If the field is filled in with the name 
                             of a column, it will be a delta-driven one and the column chosen will be used to order the 
                             descriptive rows of the same business key to compute a unique hash. Otherwise, it will be a 
                             standard multi-active satellite and all the records will be inserted every load.
        
        Returns:
            The updated satellite mapping entity as a dictionary.
        """
        try:
            logger.info(
                "update_staging_table_satellite_mapping: projectName=%s, sourceSystemIdOrName=%s, dataPackageIdOrName=%s, "
                "stagingTableIdOrName=%s, satelliteMappingIdOrName=%s, satelliteName=%s, isMultiActive=%s",
                projectName,
                sourceSystemIdOrName,
                dataPackageIdOrName,
                stagingTableIdOrName,
                satelliteMappingIdOrName,
                satelliteName,
                isMultiActive,
            )

            # Get project ID from project name
            project_id = client.projects.get_by_name(projectName)
            logger.debug("Found project ID: %s for project: %s", project_id, projectName)

            # Resolve source system and data package IDs
            source_system_id = _resolve_source_system_id(client, project_id, sourceSystemIdOrName)
            data_package_id = _resolve_data_package_id(client, project_id, source_system_id, dataPackageIdOrName)

            # Resolve staging table ID if needed
            table_id = _resolve_staging_table_id(
                client, project_id, source_system_id, data_package_id, stagingTableIdOrName
            )

            # Get all mappings for the staging table to find the satellite mapping
            mappings_response = client.source_systems.get_staging_table_mappings(
                project_id, source_system_id, data_package_id, table_id, index=0, limit=_MAX_LIMIT
            )

            # Find the satellite mapping by ID or name
            satellite_mapping_data = None
            satellite_mapping_id = None
            for mapping_data in mappings_response.mappings_list:
                mapping_id = mapping_data.get("id")
                mapping_name = mapping_data.get("name", "")
                mapping_type = mapping_data.get("mappingType", "")
                
                if mapping_type == "Satellite" and (mapping_id == satelliteMappingIdOrName or mapping_name == satelliteMappingIdOrName):
                    satellite_mapping_data = mapping_data
                    satellite_mapping_id = mapping_id
                    break

            if not satellite_mapping_data:
                raise ValueError(f"Satellite mapping '{satelliteMappingIdOrName}' not found in staging table mappings")

            # Validate and parse the satellite mapping
            satellite_mapping = SatelliteMapping.model_validate(satellite_mapping_data)
            parent_mapping_id = satellite_mapping.satelliteParentMappingId

            # Find parent mapping to determine its type
            parent_mapping = None
            for mapping_data in mappings_response.mappings_list:
                if mapping_data.get("id") == parent_mapping_id:
                    parent_mapping = mapping_data
                    break

            if not parent_mapping:
                raise ValueError(f"Parent mapping '{parent_mapping_id}' not found for satellite mapping")

            parent_mapping_type = parent_mapping.get("mappingType", "").lower()
            
            if parent_mapping_type not in ("hub", "link"):
                raise ValueError(f"Invalid parent mapping type '{parent_mapping_type}' for satellite mapping. Must be 'Hub' or 'Link'")

            # Resolve column names to column URLs
            satellite_column_urls = _resolve_satellite_columns(
                client, project_id, source_system_id, data_package_id, table_id, columnNames
            )

            # Build staging table URL
            base_url = _get_base_url(client)
            staging_table_url = _build_data_package_table_url(
                base_url, project_id, source_system_id, data_package_id, table_id
            )

            # Build subSequenceColumn URL if provided
            sub_sequence_column_url = None
            if subSequenceColumn:
                sub_sequence_column_url = _build_data_package_column_url(
                    base_url, project_id, source_system_id, data_package_id, table_id, subSequenceColumn
                )

            logger.debug(
                "Update satellite mapping - parent_type: %s, parent_mapping_id: %s, satellite_mapping_id: %s, columns: %d, subSequenceColumn: %s",
                parent_mapping_type,
                parent_mapping_id,
                satellite_mapping_id,
                len(satellite_column_urls),
                sub_sequence_column_url,
            )

            # Update the satellite mapping
            updated_satellite_mapping = client.mappings.update_satellite_mapping(
                project_id=project_id,
                satellite_mapping_id=satellite_mapping_id,
                parent_mapping_id=parent_mapping_id,
                parent_type=parent_mapping_type,
                satellite_name=satelliteName,
                satellite_columns=satellite_column_urls,
                staging_table_url=staging_table_url,
                is_multi_active=isMultiActive,
                sub_sequence_column_url=sub_sequence_column_url,
            )

            # Return the updated satellite mapping as a dictionary
            return updated_satellite_mapping.model_dump(mode="json", exclude_none=True)
        except Exception as exc:  # noqa: BLE001
            logger.exception("update_staging_table_satellite_mapping failed")
            raise
