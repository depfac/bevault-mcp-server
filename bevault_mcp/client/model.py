"""Model client for hubs, links, satellites, etc."""
import logging
from typing import Optional

from ..models import (
    Hub,
    Link,
    Satellite,
    SearchParams,
    SearchResponse,
    CreateHubRequest,
    CreateLinkRequest,
)
from .base import BaseClient
from .utils import is_guid

logger = logging.getLogger(__name__)


class ModelClient(BaseClient):
    """Client for model operations (hubs, links, satellites, search)."""

    @BaseClient._retry_decorator()
    def search(self, params: SearchParams, project_id: Optional[str] = None) -> SearchResponse:
        """Search model entities. If project_id is None, uses the configured project ID."""
        query = {
            "index": params.index,
            "limit": params.limit,
            "searchString": params.searchString,
            "includeHubs": str(params.includeHubs).lower(),
            "includeLinks": str(params.includeLinks).lower(),
            "includeSatellites": str(params.includeSatellites).lower(),
            "includeReferenceTables": str(params.includeReferenceTables).lower(),
        }
        path = f"/metavault/api/projects/{project_id}/model"
        logger.debug("GET %s params=%s", path, query)
        resp = self._client.get(path, params=query, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return SearchResponse.model_validate(data)

    @BaseClient._retry_decorator()
    def create_hub(self, project_id: str, hub_request: CreateHubRequest) -> Hub:
        """Create a hub in a project. Returns the created hub entity."""
        path = f"/metavault/api/projects/{project_id}/model/hubs"
        logger.debug("POST %s body=%s", path, hub_request.model_dump(mode="json"))
        resp = self._client.post(
            path,
            json=hub_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return Hub.model_validate(data)

    @BaseClient._retry_decorator()
    def get_hub_by_name(self, project_id: str, hub_name: str) -> Hub:
        """Get hub by name in a project. Returns the hub entity."""
        path = f"/metavault/api/projects/{project_id}/model/hubs/{hub_name}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return Hub.model_validate(data)

    def construct_hub_url(self, project_id: str, hub_id: str) -> str:
        """Construct the hub URL for a given project and hub ID."""
        base_url = self._settings.bevault_base_url.rstrip("/")
        return f"{base_url}/metavault/api/projects/{project_id}/model/hubs/{hub_id}"

    @BaseClient._retry_decorator()
    def get_hub_by_id(self, project_id: str, hub_id: str) -> Hub:
        """Get hub by ID in a project. Returns the hub entity."""
        path = f"/metavault/api/projects/{project_id}/model/hubs/{hub_id}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return Hub.model_validate(data)

    @BaseClient._retry_decorator()
    def get_link_by_id(self, project_id: str, link_id: str) -> Link:
        """Get link by ID in a project. Returns the link entity."""
        path = f"/metavault/api/projects/{project_id}/model/links/{link_id}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return Link.model_validate(data)

    @BaseClient._retry_decorator()
    @BaseClient._retry_decorator()
    def get_link_by_name(self, project_id: str, link_name: str) -> Link:
        """Get link by name in a project. Returns the link entity."""
        path = f"/metavault/api/projects/{project_id}/model/links/{link_name}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return Link.model_validate(data)

    def _resolve_hub_id(self, project_id: str, hub_id_or_name: str) -> str:
        """Resolve hub ID from either ID or name."""
        if is_guid(hub_id_or_name):
            return hub_id_or_name
        hub = self.get_hub_by_name(project_id, hub_id_or_name)
        return hub.id

    def _resolve_link_id(self, project_id: str, link_id_or_name: str) -> str:
        """Resolve link ID from either ID or name."""
        if is_guid(link_id_or_name):
            return link_id_or_name
        link = self.get_link_by_name(project_id, link_id_or_name)
        return link.id

    @BaseClient._retry_decorator()
    def create_link(self, project_id: str, link_request: CreateLinkRequest) -> Link:
        """Create a link in a project. Returns the created link entity."""
        path = f"/metavault/api/projects/{project_id}/model/links"
        logger.debug("POST %s body=%s", path, link_request.model_dump(mode="json"))
        resp = self._client.post(
            path,
            json=link_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return Link.model_validate(data)

    @BaseClient._retry_decorator()
    def update_hub(self, project_id: str, hub_id_or_name: str, hub_request: CreateHubRequest) -> Hub:
        """Update a hub in a project. Returns the updated hub entity."""
        hub_id = self._resolve_hub_id(project_id, hub_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/hubs/{hub_id}"
        logger.debug("PUT %s body=%s", path, hub_request.model_dump(mode="json"))
        resp = self._client.put(
            path,
            json=hub_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return Hub.model_validate(data)

    @BaseClient._retry_decorator()
    def delete_hub(self, project_id: str, hub_id_or_name: str) -> None:
        """Delete a hub from a project."""
        hub_id = self._resolve_hub_id(project_id, hub_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/hubs/{hub_id}"
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()

    @BaseClient._retry_decorator()
    def update_link(self, project_id: str, link_id_or_name: str, link_request: CreateLinkRequest) -> Link:
        """Update a link in a project. Returns the updated link entity."""
        link_id = self._resolve_link_id(project_id, link_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/links/{link_id}"
        logger.debug("PUT %s body=%s", path, link_request.model_dump(mode="json"))
        resp = self._client.put(
            path,
            json=link_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return Link.model_validate(data)

    @BaseClient._retry_decorator()
    def delete_link(self, project_id: str, link_id_or_name: str) -> None:
        """Delete a link from a project."""
        link_id = self._resolve_link_id(project_id, link_id_or_name)
        path = f"/metavault/api/projects/{project_id}/model/links/{link_id}"
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()

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
            raise ValueError(f"Invalid parent_type '{parent_type}'. Must be 'hub' or 'link'")
        
        path = f"/metavault/api/projects/{project_id}/model/{parent_type}s/{parent_id}/satellites/{satellite_id}"
        query = {"expand": "parent"}
        logger.debug("GET %s params=%s", path, query)
        resp = self._client.get(path, params=query, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return Satellite.model_validate(data)
