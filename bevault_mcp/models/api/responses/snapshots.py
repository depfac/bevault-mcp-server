"""Snapshots response models."""
from typing import List

from pydantic import BaseModel, Field

from ..entities.snapshot import Snapshot
from .base import PaginatedResponse


class Snapshots(BaseModel):
    """Container for snapshots list."""

    snapshots: List[Snapshot] = Field(alias="snapshots")


class SnapshotsResponse(PaginatedResponse):
    """Response model for snapshots listing."""

    embedded: Snapshots = Field(alias="_embedded")

    @property
    def _embedded(self) -> Snapshots:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def snapshots(self) -> List[Snapshot]:
        """Convenience property to directly access the snapshots list."""
        return self.embedded.snapshots
