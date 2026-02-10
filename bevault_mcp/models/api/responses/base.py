"""Base response models."""
from typing import Any

from pydantic import BaseModel, Field

from ..base import PaginatedResponseMixin


class PaginatedResponse(PaginatedResponseMixin, BaseModel):
    """Base class for paginated API responses."""

    sort: list[Any] = Field(default_factory=list)
    index: int
    limit: int
    total: int
    filter: str | None = None
    expand: list[str] = Field(default_factory=list)

