"""Staging table mappings response models."""
from typing import Any, List

from pydantic import BaseModel, Field, model_validator

from .base import PaginatedResponse


class Mappings(BaseModel):
    """Embedded mappings container."""

    mappings: List[dict] = Field(default_factory=list, alias="mappings")


class StagingTableMappingsResponse(PaginatedResponse):
    """Response model for staging table mappings listing."""

    embedded: Mappings = Field(alias="_embedded")

    @model_validator(mode="before")
    @classmethod
    def parse_mappings(cls, data: Any) -> Any:
        """Ensure mappings are stored as dicts for later parsing."""
        # Don't parse here - we'll parse in the tool based on mappingType
        return data

    @property
    def _embedded(self) -> Mappings:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def mappings_list(self) -> List[dict]:
        """Convenience property to directly access the mappings list."""
        return self.embedded.mappings
