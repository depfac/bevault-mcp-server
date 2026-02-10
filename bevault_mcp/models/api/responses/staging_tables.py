"""Staging tables response models."""

from typing import List

from pydantic import BaseModel, Field

from ..entities.staging_table import StagingTable
from .base import PaginatedResponse


class StagingTables(BaseModel):
    """Embedded staging tables container."""

    dataPackageTables: List[StagingTable] = Field(
        default_factory=list, alias="dataPackageTables"
    )


class StagingTablesResponse(PaginatedResponse):
    """Response model for staging tables listing."""

    embedded: StagingTables = Field(alias="_embedded")

    @property
    def _embedded(self) -> StagingTables:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def tables(self) -> List[StagingTable]:
        """Convenience property to directly access the staging tables list."""
        return self.embedded.dataPackageTables
