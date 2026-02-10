"""Search response models."""
from typing import List

from pydantic import BaseModel, Field

from ..entities import ModelEntity
from .base import PaginatedResponse


class EmbeddedEntities(BaseModel):
    """Embedded entities container."""

    entities: List[ModelEntity]


class SearchResponse(PaginatedResponse):
    """Response model for search operations."""

    embedded: EmbeddedEntities = Field(alias="_embedded")

    @property
    def _embedded(self) -> EmbeddedEntities:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def entities(self) -> List[ModelEntity]:
        """Convenience property to directly access the entities list."""
        return self.embedded.entities

