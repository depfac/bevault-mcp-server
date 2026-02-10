"""Information marts client."""
import logging
from typing import Any, Dict, Optional

from ..models import (
    CreateInformationMartRequest,
    CreateInformationMartScriptRequest,
    InformationMart,
    InformationMartScript,
    InformationMartsResponse,
    SnapshotsResponse,
    UpdateInformationMartScriptRequest,
)
from .base import BaseClient
from .utils import is_guid

logger = logging.getLogger(__name__)


class InformationMartsClient(BaseClient):
    """Client for information marts operations."""

    @BaseClient._retry_decorator()
    def search(
        self, project_id: str, index: int = 0, limit: int = 10, filter: Optional[str] = None
    ) -> InformationMartsResponse:
        """Search information marts in a project."""
        query: Dict[str, Any] = {"index": index, "limit": limit}
        if filter:
            query["filter"] = filter
        path = f"/metavault/api/projects/{project_id}/informationmarts"
        logger.debug("GET %s params=%s", path, query)
        resp = self._client.get(path, params=query, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return InformationMartsResponse.model_validate(data)

    @BaseClient._retry_decorator()
    def get_information_mart_by_id(self, project_id: str, information_mart_id: str) -> InformationMart:
        """Get information mart by ID in a project. Returns the information mart entity."""
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return InformationMart.model_validate(data)

    def _resolve_information_mart_id(self, project_id: str, information_mart_id_or_name: str) -> str:
        """Resolve information mart ID from either ID or name."""
        if is_guid(information_mart_id_or_name):
            return information_mart_id_or_name
        # Search for information mart by name
        result = self.search(project_id, index=0, limit=1000, filter=f"name contains {information_mart_id_or_name}")
        for im in result.information_marts:
            if im.name == information_mart_id_or_name:
                return im.id
        raise ValueError(f"Information mart '{information_mart_id_or_name}' not found")

    @BaseClient._retry_decorator()
    def get_scripts(
        self, project_id: str, information_mart_id: str, index: int = 0, limit: int = 1000
    ) -> list[InformationMartScript]:
        """Get scripts for an information mart. Returns list of scripts."""
        # The scripts are embedded in the information mart response
        # We can get them by fetching the information mart
        im = self.get_information_mart_by_id(project_id, information_mart_id)
        return im.scripts

    def _resolve_script_id(self, project_id: str, information_mart_id: str, script_id_or_name: str) -> str:
        """Resolve script ID from either ID or name."""
        if is_guid(script_id_or_name):
            return script_id_or_name
        # Get scripts list and find by name
        scripts = self.get_scripts(project_id, information_mart_id)
        for script in scripts:
            if script.name == script_id_or_name:
                return script.id
        raise ValueError(f"Script '{script_id_or_name}' not found in information mart '{information_mart_id}'")

    @BaseClient._retry_decorator()
    def get_script(
        self, project_id: str, information_mart_id: str, script_id: str
    ) -> InformationMartScript:
        """Get a script by ID in an information mart. Returns the script entity with full metadata."""
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}/scripts/{script_id}"
        logger.debug("GET %s", path)
        resp = self._client.get(path, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return InformationMartScript.model_validate(data)

    @BaseClient._retry_decorator()
    def get_snapshots(
        self, project_id: str, index: int = 0, limit: int = 1000000
    ) -> SnapshotsResponse:
        """Get snapshots for a project. Returns paginated list of snapshots."""
        query: Dict[str, Any] = {"index": index, "limit": limit}
        path = f"/metavault/api/projects/{project_id}/model/snapshots"
        logger.debug("GET %s params=%s", path, query)
        resp = self._client.get(path, params=query, headers=self._get_auth_headers())
        resp.raise_for_status()
        data = resp.json()
        return SnapshotsResponse.model_validate(data)

    def _resolve_snapshot_id(self, project_id: str, snapshot_id_or_name: str) -> str:
        """Resolve snapshot ID from either ID or name."""
        if is_guid(snapshot_id_or_name):
            return snapshot_id_or_name
        # Get snapshots list and find by name
        result = self.get_snapshots(project_id, index=0, limit=1000000)
        for snapshot in result.snapshots:
            if snapshot.name == snapshot_id_or_name:
                return snapshot.id
        raise ValueError(f"Snapshot '{snapshot_id_or_name}' not found")

    @BaseClient._retry_decorator()
    def create(
        self, project_id: str, information_mart_request: CreateInformationMartRequest
    ) -> InformationMart:
        """Create an information mart in a project. Returns the created information mart entity."""
        path = f"/metavault/api/projects/{project_id}/informationmarts"
        logger.debug("POST %s body=%s", path, information_mart_request.model_dump(mode="json"))
        resp = self._client.post(
            path,
            json=information_mart_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return InformationMart.model_validate(data)

    @BaseClient._retry_decorator()
    def update(
        self,
        project_id: str,
        information_mart_id_or_name: str,
        information_mart_request: CreateInformationMartRequest,
    ) -> InformationMart:
        """Update an information mart in a project. Returns the updated information mart entity."""
        information_mart_id = self._resolve_information_mart_id(project_id, information_mart_id_or_name)
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}"
        logger.debug("PUT %s body=%s", path, information_mart_request.model_dump(mode="json"))
        resp = self._client.put(
            path,
            json=information_mart_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return InformationMart.model_validate(data)

    @BaseClient._retry_decorator()
    def delete(self, project_id: str, information_mart_id_or_name: str) -> None:
        """Delete an information mart from a project."""
        information_mart_id = self._resolve_information_mart_id(project_id, information_mart_id_or_name)
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}"
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()

    def _calculate_next_order(self, project_id: str, information_mart_id: str) -> int:
        """Calculate the next order value (max order + 1) for scripts in an information mart."""
        scripts = self.get_scripts(project_id, information_mart_id)
        if not scripts:
            return 0
        max_order = max(script.order for script in scripts)
        return max_order + 1

    @BaseClient._retry_decorator()
    def create_script(
        self,
        project_id: str,
        information_mart_id: str,
        script_request: CreateInformationMartScriptRequest,
    ) -> InformationMartScript:
        """Create a script in an information mart. Returns the created script entity."""
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}/scripts"
        logger.debug("POST %s body=%s", path, script_request.model_dump(mode="json"))
        resp = self._client.post(
            path,
            json=script_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return InformationMartScript.model_validate(data)

    @BaseClient._retry_decorator()
    def update_script(
        self,
        project_id: str,
        information_mart_id: str,
        script_id: str,
        script_request: UpdateInformationMartScriptRequest,
    ) -> InformationMartScript:
        """Update a script's metadata (excluding code) in an information mart. Returns the updated script entity."""
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}/scripts/{script_id}"
        logger.debug("PUT %s body=%s", path, script_request.model_dump(mode="json"))
        resp = self._client.put(
            path,
            json=script_request.model_dump(mode="json", exclude_none=True),
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return InformationMartScript.model_validate(data)

    @BaseClient._retry_decorator()
    def update_script_code(
        self,
        project_id: str,
        information_mart_id: str,
        script_id: str,
        code: str,
    ) -> InformationMartScript:
        """Update a script's code only. Fetches existing script first, then updates with full payload. Returns the updated script entity."""
        # Fetch existing script to get all metadata
        existing_script = self.get_script(project_id, information_mart_id, script_id)
        
        # Create updated script dict with new code
        script_data = existing_script.model_dump(mode="json", exclude_none=True)
        script_data["code"] = code
        
        # Send PUT request with full payload
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}/scripts/{script_id}"
        logger.debug("PUT %s body=%s (code updated)", path, script_data)
        resp = self._client.put(
            path,
            json=script_data,
            headers=self._get_auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        return InformationMartScript.model_validate(data)

    @BaseClient._retry_decorator()
    def delete_script(
        self,
        project_id: str,
        information_mart_id: str,
        script_id: str,
    ) -> None:
        """Delete a script from an information mart."""
        path = f"/metavault/api/projects/{project_id}/informationmarts/{information_mart_id}/scripts/{script_id}"
        logger.debug("DELETE %s", path)
        resp = self._client.delete(path, headers=self._get_auth_headers())
        resp.raise_for_status()
