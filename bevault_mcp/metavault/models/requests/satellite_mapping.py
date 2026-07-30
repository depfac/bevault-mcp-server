"""Satellite mapping request models."""

from typing import List, Optional

from pydantic import field_validator

from bevault_mcp.shared.utils import (
    SATELLITE_TECHNICAL_NAME_MAX_LENGTH,
    validate_business_name,
    validate_technical_name,
)

from ..api.base import BeVaultRequest


class CreateSatelliteMappingRequest(BeVaultRequest):
    """Request model for creating or updating a satellite mapping."""

    satelliteName: str
    satelliteBusinessName: str
    satelliteColumns: List[str]
    stagingTable: str
    isMultiActive: bool = False
    subSequenceColumn: Optional[str] = None

    @field_validator("satelliteName")
    @classmethod
    def validate_satellite_name(cls, v: str) -> str:
        """Validate satellite technical name constraints."""
        return validate_technical_name(
            v,
            entity_label="Satellite",
            max_length=SATELLITE_TECHNICAL_NAME_MAX_LENGTH,
        )

    @field_validator("satelliteBusinessName")
    @classmethod
    def validate_satellite_business_name(cls, v: str) -> str:
        """Validate satellite business name is non-empty."""
        return validate_business_name(v, field_label="satelliteBusinessName")
