"""Information marts response models."""

from typing import List

from pydantic import BaseModel, Field

from ..entities.information_mart import InformationMart
from .base import PaginatedResponse


class InformationMarts(BaseModel):
    """Container for information marts list."""

    informationMarts: List[InformationMart] = Field(alias="informationMarts")


class InformationMartsResponse(PaginatedResponse):
    """Response model for information marts listing."""

    embedded: InformationMarts = Field(alias="_embedded")

    @property
    def _embedded(self) -> InformationMarts:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def information_marts(self) -> List[InformationMart]:
        """Convenience property to directly access the information marts list."""
        return self.embedded.informationMarts
