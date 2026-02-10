"""Source systems client."""
import logging
from typing import Any, Dict, Optional

from ..models import (
    CreateDataPackageRequest,
    CreateSourceSystemRequest,
    CreateStagingTableRequest,
    DataPackage,
    SourceSystemsResponse,
    SourceSystem,
    StagingTable,
)
from ..models.api.entities.staging_table import StagingTableColumn
from ..models.requests.staging_table import UpdateStagingTableColumnRequest
from ..models.api.responses.staging_tables import StagingTablesResponse
from ..models.api.responses.staging_table_mappings import StagingTableMappingsResponse
from ..models.api.entities.mapping import HubMapping, LinkMapping, SatelliteMapping
from .base import BaseClient
from .utils import is_guid

logger = logging.getLogger(__name__)


class SourceSystemsClient(BaseClient):
    """Client for source systems operations."""

    @BaseClient._retry_decorator()
    def create(self, project_id: str, source_system_request: CreateSourceSystemRequest) -> SourceSystem:
        """Create a source system in a project. Returns the created source system entity."""
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems"
        logger.debug("POST %s body=%s", path, source_system_request.model_dump(mode="json"))
        resp = self._client.post(
            path,
            json=source_system_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return SourceSystem.model_validate(data)

    @BaseClient._retry_decorator()
    def get_source_system_by_name(self, project_id: str, source_system_name: str) -> SourceSystem:
        """Get source system by name in a project. Returns the source system entity."""
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_name}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return SourceSystem.model_validate(data)

    @BaseClient._retry_decorator()
    def get_data_package_by_name(
        self, project_id: str, source_system_id_or_name: str, data_package_name: str
    ) -> DataPackage:
        """Get data package by name in a source system. Returns the data package entity."""
        # Use the source system ID or name directly in the path - API accepts both
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_name}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return DataPackage.model_validate(data)

    def _resolve_source_system_id(self, project_id: str, source_system_id_or_name: str) -> str:
        """Resolve source system ID from either ID or name."""
        if is_guid(source_system_id_or_name):
            return source_system_id_or_name
        source_system = self.get_source_system_by_name(project_id, source_system_id_or_name)
        return source_system.id

    def _resolve_data_package_id(
        self, project_id: str, source_system_id: str, data_package_id_or_name: str
    ) -> str:
        """Resolve data package ID from either ID or name."""
        if is_guid(data_package_id_or_name):
            return data_package_id_or_name
        data_package = self.get_data_package_by_name(project_id, source_system_id, data_package_id_or_name)
        return data_package.id

    @BaseClient._retry_decorator()
    def create_data_package(
        self, project_id: str, source_system_id_or_name: str, data_package_request: CreateDataPackageRequest
    ) -> DataPackage:
        """Create a data package in a source system. Returns the created data package entity.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_request: Data package creation request
        """
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages"
        logger.debug("POST %s body=%s", path, data_package_request.model_dump(mode="json"))
        resp = self._client.post(
            path,
            json=data_package_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return DataPackage.model_validate(data)

    @BaseClient._retry_decorator()
    def search(
        self, project_id: str, index: int = 0, limit: int = 10, filter: Optional[str] = None
    ) -> SourceSystemsResponse:
        """Search source systems in a project."""
        query: Dict[str, Any] = {"index": index, "limit": limit}
        if filter:
            query["filter"] = filter
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems"
        logger.debug("GET %s params=%s", path, query)
        resp = self._client.get(path, params=query, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return SourceSystemsResponse.model_validate(data)

    @BaseClient._retry_decorator()
    def get_source_system_by_id(self, project_id: str, source_system_id: str) -> SourceSystem:
        """Get source system by ID in a project. Returns the source system entity."""
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return SourceSystem.model_validate(data)

    @BaseClient._retry_decorator()
    def update(
        self, project_id: str, source_system_id_or_name: str, source_system_request: CreateSourceSystemRequest
    ) -> SourceSystem:
        """Update a source system in a project. Returns the updated source system entity."""
        source_system_id = self._resolve_source_system_id(project_id, source_system_id_or_name)
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id}"
        logger.debug("PUT %s body=%s", path, source_system_request.model_dump(mode="json"))
        resp = self._client.put(
            path,
            json=source_system_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return SourceSystem.model_validate(data)

    @BaseClient._retry_decorator()
    def delete(self, project_id: str, source_system_id_or_name: str) -> None:
        """Delete a source system from a project."""
        source_system_id = self._resolve_source_system_id(project_id, source_system_id_or_name)
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id}"
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()

    @BaseClient._retry_decorator()
    def get_data_package_by_id(
        self, project_id: str, source_system_id_or_name: str, data_package_id: str
    ) -> DataPackage:
        """Get data package by ID in a source system. Returns the data package entity."""
        source_system_id = self._resolve_source_system_id(project_id, source_system_id_or_name)
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id}/datapackages/{data_package_id}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return DataPackage.model_validate(data)

    @BaseClient._retry_decorator()
    def update_data_package(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        data_package_request: CreateDataPackageRequest,
    ) -> DataPackage:
        """Update a data package in a source system. Returns the updated data package entity."""
        source_system_id = self._resolve_source_system_id(project_id, source_system_id_or_name)
        data_package_id = self._resolve_data_package_id(project_id, source_system_id, data_package_id_or_name)
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id}/datapackages/{data_package_id}"
        logger.debug("PUT %s body=%s", path, data_package_request.model_dump(mode="json"))
        resp = self._client.put(
            path,
            json=data_package_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return DataPackage.model_validate(data)

    @BaseClient._retry_decorator()
    def delete_data_package(self, project_id: str, source_system_id_or_name: str, data_package_id_or_name: str) -> None:
        """Delete a data package from a source system."""
        source_system_id = self._resolve_source_system_id(project_id, source_system_id_or_name)
        data_package_id = self._resolve_data_package_id(project_id, source_system_id, data_package_id_or_name)
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id}/datapackages/{data_package_id}"
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()

    @BaseClient._retry_decorator()
    def create_staging_table(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        staging_table_request: CreateStagingTableRequest,
    ) -> StagingTable:
        """
        Create a staging table in a data package. Returns the created staging table entity.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_id_or_name: Data package ID or name (API accepts both)
            staging_table_request: Staging table creation request
        """
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_id_or_name}/tables"
        logger.debug("POST %s body=%s", path, staging_table_request.model_dump(mode="json"))
        resp = self._client.post(
            path,
            json=staging_table_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return StagingTable.model_validate(data)

    @BaseClient._retry_decorator()
    def get_staging_tables(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        index: int = 0,
        limit: int = 1000000,
    ) -> StagingTablesResponse:
        """
        Get staging tables for a data package. Returns paginated list of staging tables.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_id_or_name: Data package ID or name (API accepts both)
            index: Pagination index (default: 0)
            limit: Maximum number of results (default: 1000000 to get all tables)
        """
        query: Dict[str, Any] = {"index": index, "limit": limit}
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_id_or_name}/tables"
        logger.debug("GET %s params=%s", path, query)
        resp = self._client.get(path, params=query, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return StagingTablesResponse.model_validate(data)

    @BaseClient._retry_decorator()
    def add_staging_table_column(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        table_id_or_name: str,
        column_request: UpdateStagingTableColumnRequest,
    ) -> StagingTableColumn:
        """
        Add a column to a staging table. Returns the created column entity.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_id_or_name: Data package ID or name (API accepts both)
            table_id_or_name: Staging table ID or name
            column_request: Column creation request (without id field)
        """
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_id_or_name}/tables/{table_id_or_name}/columns"
        logger.debug("POST %s body=%s", path, column_request.model_dump(mode="json", exclude_none=True))
        resp = self._client.post(
            path,
            json=column_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return StagingTableColumn.model_validate(data)

    @BaseClient._retry_decorator()
    def update_staging_table_column(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        column_id: str,
        column_request: UpdateStagingTableColumnRequest,
    ) -> StagingTableColumn:
        """
        Update a staging table column. Returns the updated column entity.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_id_or_name: Data package ID or name (API accepts both)
            column_id: Column ID
            column_request: Column update request (should include id field)
        """
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_id_or_name}/tables/columns/{column_id}"
        logger.debug("PUT %s body=%s", path, column_request.model_dump(mode="json", exclude_none=True))
        resp = self._client.put(
            path,
            json=column_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return StagingTableColumn.model_validate(data)

    @BaseClient._retry_decorator()
    def delete_staging_table_column(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        column_id: str,
    ) -> None:
        """
        Delete a staging table column.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_id_or_name: Data package ID or name (API accepts both)
            column_id: Column ID
        """
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_id_or_name}/tables/columns/{column_id}"
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()

    @BaseClient._retry_decorator()
    def get_staging_table(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        table_id_or_name: str,
    ) -> StagingTable:
        """
        Get a staging table by ID or name. Returns the staging table entity.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_id_or_name: Data package ID or name (API accepts both)
            table_id_or_name: Staging table ID or name (API accepts both)
        """
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_id_or_name}/tables/{table_id_or_name}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return StagingTable.model_validate(data)

    @BaseClient._retry_decorator()
    def get_staging_table_mappings(
        self,
        project_id: str,
        source_system_id_or_name: str,
        data_package_id_or_name: str,
        table_id_or_name: str,
        index: int = 0,
        limit: int = 1000000,
    ) -> StagingTableMappingsResponse:
        """
        Get mappings for a staging table. Returns paginated list of mappings.
        
        Args:
            project_id: Project ID
            source_system_id_or_name: Source system ID or name (API accepts both)
            data_package_id_or_name: Data package ID or name (API accepts both)
            table_id_or_name: Staging table ID or name (API accepts both)
            index: Pagination index (default: 0)
            limit: Maximum number of results (default: 1000000 to get all mappings)
        """
        query: Dict[str, Any] = {"index": index, "limit": limit}
        path = f"/metavault/api/projects/{project_id}/metavault/sourcesystems/{source_system_id_or_name}/datapackages/{data_package_id_or_name}/tables/{table_id_or_name}/mappings"
        logger.debug("GET %s params=%s", path, query)
        resp = self._client.get(path, params=query, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return StagingTableMappingsResponse.model_validate(data)

