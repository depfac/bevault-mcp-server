"""Mappings client."""

import logging
from typing import List

from ..models.api.entities.mapping import HubMapping, LinkMapping, SatelliteMapping
from .base import BaseClient

logger = logging.getLogger(__name__)


class MappingsClient(BaseClient):
    """Client for mapping operations."""

    @BaseClient._retry_decorator()
    def create_hub_mapping(
        self,
        project_id: str,
        hub_url: str,
        data_package_table_url: str,
        data_package_column_url: str,
        is_full_load: bool = False,
        expect_null_business_key: bool = False,
    ) -> HubMapping:
        """
        Create a hub mapping for a staging table column.

        Args:
            project_id: Project ID
            hub_url: Full URL to the hub (e.g., "{base_url}/metavault/api/projects/{project_id}/model/hubs/{hub_id_or_name}")
            data_package_table_url: Full URL to the data package table
            data_package_column_url: Full URL to the data package column
            is_full_load: Whether this is a full load (default: False)
            expect_null_business_key: Whether null business keys are expected (default: False)

        Returns:
            The created hub mapping entity
        """
        path = f"/metavault/api/projects/{project_id}/mappings/hubs"
        payload = {
            "hub": hub_url,
            "isFullLoad": is_full_load,
            "expectNullBusinessKey": expect_null_business_key,
            "dataPackageTable": data_package_table_url,
            "dataPackageColumn": data_package_column_url,
        }
        logger.debug("POST %s body=%s", path, payload)
        resp = self._client.post(
            path,
            json=payload,
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return HubMapping.model_validate(data)

    @BaseClient._retry_decorator()
    def create_link_mapping(
        self,
        project_id: str,
        link_url: str,
        data_package_table_url: str,
        is_full_load: bool = True,
        hub_references_details: List[dict] | None = None,
        link_mapping_dependent_child_columns: List[dict] | None = None,
        link_mapping_data_columns: List[dict] | None = None,
    ) -> LinkMapping:
        """
        Create a link mapping for a staging table.

        Args:
            project_id: Project ID
            link_url: Full URL to the link (e.g., "{base_url}/metavault/api/projects/{project_id}/model/links/{link_id_or_name}")
            data_package_table_url: Full URL to the data package table
            is_full_load: Whether this is a full load (default: True)
            hub_references_details: List of objects with "hubMapping" (URL) and "hubReference" (URL)
            link_mapping_dependent_child_columns: List of objects with "linkColumnId" (ID) and "dataPackageTableColumn" (URL)
            link_mapping_data_columns: List of objects with "linkColumnId" (ID) and "dataPackageTableColumn" (URL)

        Returns:
            The created link mapping entity (excluding _links).
        """
        path = f"/metavault/api/projects/{project_id}/mappings/links"
        payload = {
            "link": link_url,
            "isFullLoad": is_full_load,
            "dataPackageTable": data_package_table_url,
        }
        if hub_references_details:
            payload["hubReferencesDetails"] = hub_references_details
        if link_mapping_dependent_child_columns:
            payload["linkMappingDependentChildColumns"] = (
                link_mapping_dependent_child_columns
            )
        if link_mapping_data_columns:
            payload["linkMappingDataColumns"] = link_mapping_data_columns

        logger.debug("POST %s body=%s", path, payload)
        headers = self._get_auth_headers()
        logger.debug("Headers: %s", headers)
        resp = self._client.post(
            path,
            json=payload,
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return LinkMapping.model_validate(data)

    @BaseClient._retry_decorator()
    def create_satellite_mapping(
        self,
        project_id: str,
        parent_mapping_id: str,
        parent_type: str,
        satellite_name: str,
        satellite_columns: List[str],
        staging_table_url: str,
        is_multi_active: bool = False,
        sub_sequence_column_url: str | None = None,
    ) -> SatelliteMapping:
        """
        Create a satellite mapping for a staging table.

        Args:
            project_id: Project ID
            parent_mapping_id: ID of the parent mapping (hub or link mapping)
            parent_type: Type of parent mapping - "hub" or "link"
            satellite_name: Name of the satellite (will be prefixed with parent name)
            satellite_columns: List of column URLs
            staging_table_url: Full URL to the staging table
            is_multi_active: Whether this is a multi-active satellite (default: False)
            sub_sequence_column_url: Optional column URL for delta-driven multi-active satellites

        Returns:
            The created satellite mapping entity
        """
        if parent_type not in ("hub", "link"):
            raise ValueError(
                f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'"
            )

        path = f"/metavault/api/projects/{project_id}/mappings/{parent_type}s/{parent_mapping_id}/satellites"
        payload = {
            "satelliteColumns": satellite_columns,
            "satelliteName": satellite_name,
            "stagingTable": staging_table_url,
            "isMultiActive": is_multi_active,
        }
        if sub_sequence_column_url:
            payload["subSequenceColumn"] = sub_sequence_column_url

        logger.debug("POST %s body=%s", path, payload)
        resp = self._client.post(
            path,
            json=payload,
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return SatelliteMapping.model_validate(data)

    @BaseClient._retry_decorator()
    def update_satellite_mapping(
        self,
        project_id: str,
        satellite_mapping_id: str,
        parent_mapping_id: str,
        parent_type: str,
        satellite_name: str,
        satellite_columns: List[str],
        staging_table_url: str,
        is_multi_active: bool = False,
        sub_sequence_column_url: str | None = None,
    ) -> SatelliteMapping:
        """
        Update a satellite mapping for a staging table.

        Args:
            project_id: Project ID
            satellite_mapping_id: ID of the satellite mapping to update
            parent_mapping_id: ID of the parent mapping (hub or link mapping)
            parent_type: Type of parent mapping - "hub" or "link"
            satellite_name: Name of the satellite (will be prefixed with parent name)
            satellite_columns: List of column URLs
            staging_table_url: Full URL to the staging table
            is_multi_active: Whether this is a multi-active satellite (default: False)
            sub_sequence_column_url: Optional column URL for delta-driven multi-active satellites

        Returns:
            The updated satellite mapping entity
        """
        if parent_type not in ("hub", "link"):
            raise ValueError(
                f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'"
            )

        path = f"/metavault/api/projects/{project_id}/mappings/{parent_type}s/{parent_mapping_id}/satellites/{satellite_mapping_id}"
        payload = {
            "satelliteColumns": satellite_columns,
            "satelliteName": satellite_name,
            "stagingTable": staging_table_url,
            "isMultiActive": is_multi_active,
        }
        if sub_sequence_column_url:
            payload["subSequenceColumn"] = sub_sequence_column_url

        logger.debug("PUT %s body=%s", path, payload)
        resp = self._client.put(
            path,
            json=payload,
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return SatelliteMapping.model_validate(data)

    @BaseClient._retry_decorator()
    def delete_mapping(self, project_id: str, path: str) -> None:
        """
        Delete a mapping by its API path.

        Args:
            project_id: Project ID
            path: Full API path to the mapping (e.g., "/metavault/api/projects/{project_id}/mappings/hubs/{mappingId}")
        """
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()
