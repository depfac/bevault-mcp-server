"""Hub entity model."""
from typing import Literal, Optional

from pydantic import BaseModel

from .base_model_entity import BaseModelEntity


class BusinessKey(BaseModel):
    """Business key entity - specific to hubs."""

    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    length: Optional[int] = None


class Hub(BaseModelEntity):
    """Hub entity with hub-specific fields."""

    entityType: Literal["Hub"] = "Hub"
    satelliteCount: Optional[int] = None
    dependentLinkCount: Optional[int] = None
    businessKey: Optional[BusinessKey] = None

