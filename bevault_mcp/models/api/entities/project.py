"""Project entity model."""

from typing import Optional

from ..base import BeVaultEntity


class Project(BeVaultEntity):
    """Project entity."""

    id: str
    name: str
    technicalName: Optional[str] = None
    displayName: Optional[str] = None
    description: Optional[str] = None
    creationDate: Optional[str] = None
    numberOfHubs: Optional[int] = None
    numberOfSources: Optional[int] = None
    numberOfDataQualityControls: Optional[int] = None
