"""Link creation request models."""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ..api.base import BeVaultRequest


class LinkType(str, Enum):
    """Link type enumeration."""

    RELATIONSHIP = "Relationship"
    HIERARCHY = "Hierarchy"
    TRANSACTION = "Transaction"
    SAME_AS = "SameAs"


class DependentChildColumn(BeVaultRequest):
    """Dependent child column model for link creation."""

    columnName: str
    dataType: str


class HubReference(BeVaultRequest):
    """Hub reference model for link creation."""

    columnName: str
    hub: str  # URL to the hub
    order: int


class CreateLinkRequest(BeVaultRequest):
    """Request model for creating a link."""

    name: str
    linkType: LinkType = LinkType.RELATIONSHIP
    dependentChildColumns: List[DependentChildColumn] = Field(default_factory=list)
    hubReferences: List[HubReference] = Field(default_factory=list)
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None

