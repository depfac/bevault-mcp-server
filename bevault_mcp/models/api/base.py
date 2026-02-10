"""Base classes and mixins for beVault API models."""
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class BeVaultApiMixin:
    """Mixin for beVault API models that strips HAL _links from responses."""

    @model_validator(mode="before")
    @classmethod
    def strip_hal_links(cls, data: Any) -> Any:
        """Remove _links field from HAL API responses."""
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if k != "_links"}
        return data


class BeVaultEntity(BeVaultApiMixin, BaseModel):
    """Base class for all beVault entity models."""

    model_config = ConfigDict(extra="ignore")


class BeVaultRequest(BaseModel):
    """Base class for beVault API request models."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class PaginatedResponseMixin(BeVaultApiMixin):
    """Mixin for paginated API responses."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

