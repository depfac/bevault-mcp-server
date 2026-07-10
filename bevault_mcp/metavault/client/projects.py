"""Projects client."""

import logging

from ..models import ProjectsResponse
from .base import BaseClient

logger = logging.getLogger(__name__)


class ProjectsClient(BaseClient):
    """Client for project-related operations."""

    @BaseClient._retry_decorator()
    def get_projects(self) -> ProjectsResponse:
        """Get list of projects the user has explicit read rights on (onlyAffected=true)."""
        query = {"onlyAffected": True}
        path = "/metavault/api/projects"
        data = self._get(path, params=query)
        return ProjectsResponse.model_validate(data)

    @BaseClient._retry_decorator()
    def get_by_name(self, project_name: str) -> str:
        """Get project ID by project name. Returns the ID of the first matching project."""
        query = {"filter": f"name eq {project_name}"}
        path = "/metavault/api/projects"
        data = self._get(path, params=query)
        projects_response = ProjectsResponse.model_validate(data)
        if projects_response.total == 0:
            raise ValueError(f"Project '{project_name}' not found")
        if projects_response.total > 1:
            logger.warning(
                "Multiple projects found with name '%s', using the first one",
                project_name,
            )
        # Access projects list directly via convenience property
        if not projects_response.projects:
            raise ValueError("No projects found in response")
        return projects_response.projects[0].id
