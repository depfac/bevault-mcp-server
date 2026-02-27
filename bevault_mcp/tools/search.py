import logging
from typing import Optional

from fastmcp import FastMCP

from ..client import BeVaultClient
from ..models import (
    Hub,
    Link,
    OptimizedEntity,
    OptimizedHub,
    OptimizedLink,
    OptimizedReferenceTable,
    OptimizedSatellite,
    OptimizedSearchResponse,
    PagingInfo,
    ReferenceTable,
    Satellite,
    SearchParams,
    SearchResponse,
)

logger = logging.getLogger(__name__)


def _transform_entity(
    entity: Hub | Link | Satellite | ReferenceTable,
    project_id: str,
    client: BeVaultClient,
    entity_lookup: dict[str, Hub | Link],  # Lookup by ID for parent resolution
) -> OptimizedEntity:
    """Transform a full entity to an optimized entity."""
    base_data = {
        "id": entity.id,
        "name": entity.name,
        "tableName": entity.tableName,
        "businessDescription": entity.businessDescription,
        "technicalDescription": entity.technicalDescription,
    }

    if isinstance(entity, Hub):
        return OptimizedHub(
            **base_data,
            satelliteCount=entity.satelliteCount,
            dependentLinkCount=entity.dependentLinkCount,
            businessKeyLength=entity.businessKey.length if entity.businessKey else None,
        )
    elif isinstance(entity, Link):
        return OptimizedLink(
            **base_data,
            linkType=entity.linkType,
            dependentLinkCount=entity.dependentLinkCount,
        )
    elif isinstance(entity, Satellite):
        # Fetch parent name - first check if parent is in the search results
        parent_name: Optional[str] = None
        if entity.parentId and entity.parentType:
            # Check if parent is already in the search results
            parent_entity = entity_lookup.get(entity.parentId)

            if parent_entity:
                # Parent found in search results - use it directly
                parent_name = parent_entity.name
                logger.debug(
                    "Found parent %s '%s' for satellite '%s' in search results",
                    entity.parentType,
                    parent_name,
                    entity.name,
                )
            else:
                # Parent not in search results - fetch from API
                try:
                    if entity.parentType == "Hub":
                        parent_entity = client.model.get_hub_by_id(
                            project_id, entity.parentId
                        )
                        parent_name = parent_entity.name
                    elif entity.parentType == "Link":
                        parent_entity = client.model.get_link_by_id(
                            project_id, entity.parentId
                        )
                        parent_name = parent_entity.name
                    logger.debug(
                        "Fetched parent %s '%s' for satellite '%s' from API",
                        entity.parentType,
                        parent_name,
                        entity.name,
                    )
                except Exception as e:
                    logger.warning(
                        "Failed to fetch parent %s %s for satellite %s: %s",
                        entity.parentType,
                        entity.parentId,
                        entity.name,
                        e,
                    )
                    parent_name = None

        return OptimizedSatellite(
            **base_data,
            parentType=entity.parentType,
            parentName=parent_name,
            isMultiActive=entity.isMultiActive,
            mappingCount=entity.mappingCount,
        )
    elif isinstance(entity, ReferenceTable):
        return OptimizedReferenceTable(
            **base_data,
            mappingCount=entity.mappingCount,
        )
    else:
        raise ValueError(f"Unknown entity type: {type(entity)}")


def register_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    @mcp.tool()
    def search_model(
        projectName: str,
        searchString: str | None = None,
        index: int = 0,
        limit: int = 10,
        includeHubs: bool = True,
        includeLinks: bool = True,
        includeSatellites: bool = True,
        includeReferenceTables: bool = True,
    ) -> dict:
        """
        Search entities in beVault model (Hubs, Links, Satellites, ReferenceTables).
        The projectName is mandatory and should be unquoted and is case sensitive.
        Returns optimized paginated response with paging info and entities (mappings removed, business key simplified, parent names for satellites).
        """
        try:
            params = SearchParams(
                searchString=searchString,
                projectName=projectName,
                index=index,
                limit=limit,
                includeHubs=includeHubs,
                includeLinks=includeLinks,
                includeSatellites=includeSatellites,
                includeReferenceTables=includeReferenceTables,
            )
            logger.info(
                "search_model: searchString=%s, projectName=%s",
                params.searchString,
                params.projectName,
            )

            # Get project ID from project name if provided
            project_id = client.projects.get_by_name(params.projectName)
            logger.debug(
                "Found project ID: %s for project: %s",
                project_id,
                params.projectName,
            )

            # Get search results (client will use configured project_id if None)
            result: SearchResponse = client.model.search(params, project_id=project_id)

            # Build lookup dictionary for parent resolution (only Hubs and Links can be parents)
            entity_lookup: dict[str, Hub | Link] = {}
            for entity in result.entities:
                if isinstance(entity, (Hub, Link)):
                    entity_lookup[entity.id] = entity

            logger.debug(
                "Built entity lookup with %d hubs/links for parent resolution",
                len(entity_lookup),
            )

            # Transform entities to optimized format
            optimized_entities = [
                _transform_entity(entity, project_id, client, entity_lookup)
                for entity in result.entities
            ]

            # Create optimized response
            optimized_response = OptimizedSearchResponse(
                paging=PagingInfo(
                    sort=result.sort,
                    index=result.index,
                    limit=result.limit,
                    total=result.total,
                    filter=result.filter,
                    expand=result.expand,
                ),
                entities=optimized_entities,
            )

            return optimized_response.model_dump(mode="json")
        except Exception:  # noqa: BLE001
            logger.exception("search_model failed")
            raise
