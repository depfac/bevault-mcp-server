"""Source system entity."""
from typing import Optional

from ..base import BeVaultEntity


class SourceSystem(BeVaultEntity):
    """Source system entity."""

    id: str
    name: str
    code: Optional[str] = None
    version: Optional[str] = None
    qualityType: Optional[str] = None  # API returns string like "Good", "Excellent", etc.
    dataSteward: Optional[str] = None
    systemAdministrator: Optional[str] = None
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None


class DataPackage(BeVaultEntity):
    """Data package entity."""

    id: str
    name: str
    deliverySchedule: Optional[str] = None
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None
    refreshType: Optional[str] = None
    formatInfo: Optional[str] = None
    expectedQuality: Optional[str] = None  # API returns as string

