"""Model client for hubs, links, satellites, etc."""

from typing import Any, Callable, Type, TypeVar

from pydantic import BaseModel

from ..models import (
    Hub,
    Link,
    PitTable,
    Satellite,
    SearchParams,
    SearchResponse,
    CreateHubRequest,
    CreateLinkRequest,
)
from .base import BaseClient
from .utils import is_guid

T = TypeVar("T", bound=BaseModel)


class ModelClient(BaseClient):
    """Client for model operations (hubs, links, satellites, search)."""

    @BaseClient._retry_decorator()
    def search(self, params: SearchParams, project_id: str) -> SearchResponse:
        """Search model entities."""
        query = {
            "index": params.index,
            "limit": params.limit,
            "searchString": params.searchString or "",
            "includeHubs": str(params.includeHubs).lower(),
            "includeLinks": str(params.includeLinks).lower(),
            "includeSatellites": str(params.includeSatellites).lower(),
            "includeReferenceTables": str(params.includeReferenceTables).lower(),
        }
        path = f"/metavault/api/projects/{project_id}/model"
        data = self._get(path, params=query)
        return SearchResponse.model_validate(data)

    @BaseClient._retry_decorator()
    def create_hub(self, project_id: str, hub_request: CreateHubRequest) -> Hub:
        """Create a hub in a project. Returns the created hub entity."""
        path = f"/metavault/api/projects/{project_id}/model/hubs"
        body = hub_request.model_dump(mode="json", exclude_none=True)
        return self._create_entity(path, body, Hub)

    @BaseClient._retry_decorator()
    def get_hub(
        self,
        project_id: str,
        hub_id_or_name: str,
        expand: list[str] | None = None,
    ) -> Hub:
        """Get hub by ID or name in a project. Returns the hub entity.

        Args:
            project_id: Project ID
            hub_id_or_name: Hub ID or name
            expand: Optional list of links to expand (e.g. ["pitTables"] for embedded pit tables)
        """
        path = f"/metavault/api/projects/{project_id}/model/hubs/{hub_id_or_name}"
        params = None
        headers = None
        if expand:
            params = {"expand": ",".join(expand)}
            headers = {"Accept": "application/hal+json"}
        data = self._get(path, params=params, headers=headers)
        return Hub.model_validate(data)

    def construct_hub_url(self, project_id: str, hub_id: str) -> str:
        """Construct the hub URL for a given project and hub ID."""
        base_url = self._settings.bevault_base_url.rstrip("/")
        return f"{base_url}/metavault/api/projects/{project_id}/model/hubs/{hub_id}"

    @BaseClient._retry_decorator()
    def get_link(
        self,
        project_id: str,
        link_id_or_name: str,
        expand: list[str] | None = None,
    ) -> Link:
        """Get link by ID or name in a project. Returns the link entity.

        Args:
            project_id: Project ID
            link_id_or_name: Link ID or name
            expand: Optional list of links to expand (e.g. ["pitTables"] for embedded pit tables)
        """
        path = f"/metavault/api/projects/{project_id}/model/links/{link_id_or_name}"
        params = None
        headers = None
        if expand:
            params = {"expand": ",".join(expand)}
            headers = {"Accept": "application/hal+json"}
        data = self._get(path, params=params, headers=headers)
        return Link.model_validate(data)

    def _resolve_id(
        self,
        project_id: str,
        id_or_name: str,
        get_entity: Callable[[str, str], Any],
    ) -> str:
        """Resolve entity ID from either ID or name."""
        if is_guid(id_or_name):
            return id_or_name
        entity = get_entity(project_id, id_or_name)
        return entity.id

    def _resolve_hub_id(self, project_id: str, hub_id_or_name: str) -> str:
        """Resolve hub ID from either ID or name."""
        return self._resolve_id(project_id, hub_id_or_name, self.get_hub)

    def _resolve_link_id(self, project_id: str, link_id_or_name: str) -> str:
        """Resolve link ID from either ID or name."""
        return self._resolve_id(project_id, link_id_or_name, self.get_link)

    def _create_entity(
        self, path: str, request_body: dict, response_model: Type[T]
    ) -> T:
        """POST path with body; return response validated as response_model."""
        data = self._post(path, request_body)
        return response_model.model_validate(data)

    def _update_entity(
        self, path: str, request_body: dict, response_model: Type[T]
    ) -> T:
        """PUT path with body; return response validated as response_model."""
        data = self._put(path, request_body)
        return response_model.model_validate(data)

    def _delete_entity(self, path: str) -> None:
        """DELETE path."""
        self._delete(path)

    @BaseClient._retry_decorator()
    def create_link(self, project_id: str, link_request: CreateLinkRequest) -> Link:
        """Create a link in a project. Returns the created link entity."""
        path = f"/metavault/api/projects/{project_id}/model/links"
        body = link_request.model_dump(mode="json", exclude_none=True)
        return self._create_entity(path, body, Link)

    @BaseClient._retry_decorator()
    def update_hub(
        self, project_id: str, hub_id_or_name: str, hub_request: CreateHubRequest
    ) -> Hub:
        """Update a hub in a project. Returns the updated hub entity."""
        hub_id = self._resolve_hub_id(project_id, hub_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/hubs/{hub_id}"
        body = hub_request.model_dump(mode="json", exclude_none=True)
        return self._update_entity(path, body, Hub)

    @BaseClient._retry_decorator()
    def delete_hub(self, project_id: str, hub_id_or_name: str) -> None:
        """Delete a hub from a project."""
        hub_id = self._resolve_hub_id(project_id, hub_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/hubs/{hub_id}"
        self._delete_entity(path)

    @BaseClient._retry_decorator()
    def update_link(
        self, project_id: str, link_id_or_name: str, link_request: CreateLinkRequest
    ) -> Link:
        """Update a link in a project. Returns the updated link entity."""
        link_id = self._resolve_link_id(project_id, link_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/links/{link_id}"
        body = link_request.model_dump(mode="json", exclude_none=True)
        return self._update_entity(path, body, Link)

    @BaseClient._retry_decorator()
    def delete_link(self, project_id: str, link_id_or_name: str) -> None:
        """Delete a link from a project."""
        link_id = self._resolve_link_id(project_id, link_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/links/{link_id}"
        self._delete_entity(path)

    @BaseClient._retry_decorator()
    def get_satellite(
        self, project_id: str, parent_type: str, parent_id: str, satellite_id: str
    ) -> Satellite:
        """
        Get satellite by ID in a project. Returns the satellite entity with columns and parent.

        Args:
            project_id: Project ID
            parent_type: Type of parent - "hub" or "link"
            parent_id: ID of the parent hub or link
            satellite_id: ID of the satellite

        Returns:
            The satellite entity with embedded columns and parent
        """
        if parent_type not in ("hub", "link"):
            raise ValueError(
                f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'"
            )

        path = f"/metavault/api/projects/{project_id}/model/{parent_type}s/{parent_id}/satellites/{satellite_id}"
        query = {"expand": "parent"}
        data = self._get(path, params=query)
        return Satellite.model_validate(data)

    def _resolve_parent_id(
        self, project_id: str, parent_type: str, parent_id_or_name: str
    ) -> str:
        """Resolve parent (hub or link) ID from ID or name."""
        if parent_type == "hub":
            return self._resolve_hub_id(project_id, parent_id_or_name)
        if parent_type == "link":
            return self._resolve_link_id(project_id, parent_id_or_name)
        raise ValueError(
            f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'"
        )

    @BaseClient._retry_decorator()
    def create_pit_table(
        self,
        project_id: str,
        parent_type: str,
        parent_id_or_name: str,
        snapshot_id: str,
        description: str | None = None,
    ) -> PitTable:
        """Create a pit table for a hub or link. Satellites are attached automatically by beVault."""
        if parent_type not in ("hub", "link"):
            raise ValueError(
                f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'"
            )
        parent_id = self._resolve_parent_id(project_id, parent_type, parent_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/{parent_type}s/{parent_id}/pit_tables"
        body: dict[str, str] = {"snapshotId": snapshot_id}
        if description is not None:
            body["description"] = description
        data = self._post(path, body)
        return PitTable.model_validate(data)

    @BaseClient._retry_decorator()
    def delete_pit_table(
        self,
        project_id: str,
        parent_type: str,
        parent_id_or_name: str,
        pit_table_id: str,
    ) -> None:
        """Delete a pit table from a hub or link."""
        if parent_type not in ("hub", "link"):
            raise ValueError(
                f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'"
            )
        parent_id = self._resolve_parent_id(project_id, parent_type, parent_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/{parent_type}s/{parent_id}/pit_tables/{pit_table_id}"
        self._delete_entity(path)
