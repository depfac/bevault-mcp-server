"""Pit table entity model."""

from typing import List, Optional

from pydantic import BaseModel

from ..base import BeVaultEntity


class PitTableSatelliteRef(BaseModel):
    """Satellite reference within a pit table."""

    satelliteId: str
    pitTableId: str
    id: str


class PitTable(BeVaultEntity):
    """Pit table entity - Point-in-Time table for hubs and links."""

    id: str
    name: str
    description: Optional[str] = None
    satellites: List[PitTableSatelliteRef] = []
    parentType: str  # "Hub" or "Link"
