"""Source system creation request models."""
from typing import Optional

from ..api.base import BeVaultRequest


class CreateSourceSystemRequest(BeVaultRequest):
    """Request model for creating a source system."""

    name: str
    code: str
    version: Optional[str] = None
    qualityType: Optional[int] = None
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None
    dataSteward: Optional[str] = None
    systemAdministrator: Optional[str] = None


class CreateDataPackageRequest(BeVaultRequest):
    """Request model for creating a data package."""

    name: str
    deliverySchedule: Optional[str] = None
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None
    refreshType: Optional[str] = None
    formatInfo: Optional[str] = None
    expectedQuality: Optional[int] = None

