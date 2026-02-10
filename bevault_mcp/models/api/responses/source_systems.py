"""Source systems response models."""

from typing import List

from pydantic import BaseModel, Field

from ..entities.source_system import DataPackage, SourceSystem
from .base import PaginatedResponse


class SourceSystemWithPackages(SourceSystem):
    """Source system entity with packages from search response."""

    packages: List[DataPackage] = Field(default_factory=list)


class EmbeddedSourceSystems(BaseModel):
    """Embedded source systems container."""

    sourceSystems: List[SourceSystemWithPackages] = Field(alias="sourceSystems")


class SourceSystemsResponse(PaginatedResponse):
    """Response model for source systems listing."""

    embedded: EmbeddedSourceSystems = Field(alias="_embedded")

    @property
    def _embedded(self) -> EmbeddedSourceSystems:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def source_systems(self) -> List[SourceSystemWithPackages]:
        """Convenience property to directly access the source systems list."""
        return self.embedded.sourceSystems
