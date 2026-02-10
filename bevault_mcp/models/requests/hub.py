"""Hub creation request models."""

from typing import Optional

from pydantic import Field

from ..api.base import BeVaultRequest


class BusinessKeyRequest(BeVaultRequest):
    """Business key request model for creating hubs."""

    length: int = 255


class CreateHubRequest(BeVaultRequest):
    """Request model for creating a hub."""

    name: str
    ignoreBusinessKeyCase: bool = False
    businessKey: BusinessKeyRequest = Field(
        default_factory=lambda: BusinessKeyRequest(length=255)
    )
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None
