"""Link creation request models."""

from enum import Enum
from typing import List, Optional

from pydantic import Field, field_validator

from bevault_mcp.shared.utils import (
    LINK_TECHNICAL_NAME_MAX_LENGTH,
    validate_business_name,
    validate_technical_name,
)

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
    businessName: str
    linkType: LinkType = LinkType.RELATIONSHIP
    dependentChildColumns: List[DependentChildColumn] = Field(default_factory=list)
    hubReferences: List[HubReference] = Field(default_factory=list)
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate link technical name constraints."""
        return validate_technical_name(
            v, entity_label="Link", max_length=LINK_TECHNICAL_NAME_MAX_LENGTH
        )

    @field_validator("businessName")
    @classmethod
    def validate_business_name_field(cls, v: str) -> str:
        """Validate link business name is non-empty."""
        return validate_business_name(v)
