"""Projects response models."""

from typing import List

from pydantic import BaseModel, Field

from ..entities import Project
from .base import PaginatedResponse


class EmbeddedProjects(BaseModel):
    """Embedded projects container."""

    projects: List[Project]


class ProjectsResponse(PaginatedResponse):
    """Response model for projects listing."""

    embedded: EmbeddedProjects = Field(alias="_embedded")

    @property
    def _embedded(self) -> EmbeddedProjects:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def projects(self) -> List[Project]:
        """Convenience property to directly access the projects list."""
        return self.embedded.projects
