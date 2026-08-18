"""Hub creation request models."""

from typing import Optional

from pydantic import Field, field_validator

from bevault_mcp.shared.utils import (
    HUB_TECHNICAL_NAME_MAX_LENGTH,
    validate_business_name,
    validate_technical_name,
)

from ..api.base import BeVaultRequest


class BusinessKeyRequest(BeVaultRequest):
    """Business key request model for creating hubs."""

    length: int = 255


class CreateHubRequest(BeVaultRequest):
    """Request model for creating a hub."""

    name: str
    businessName: str
    ignoreBusinessKeyCase: bool = False
    businessKey: BusinessKeyRequest = Field(
        default_factory=lambda: BusinessKeyRequest(length=255)
    )
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate hub technical name constraints."""
        return validate_technical_name(
            v, entity_label="Hub", max_length=HUB_TECHNICAL_NAME_MAX_LENGTH
        )

    @field_validator("businessName")
    @classmethod
    def validate_business_name_field(cls, v: str) -> str:
        """Validate hub business name is non-empty."""
        return validate_business_name(v)
