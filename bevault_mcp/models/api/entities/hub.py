"""Hub entity model."""

from typing import Any, List, Literal, Optional

from pydantic import BaseModel, model_validator

from ..embedded import parse_embedded_resource
from .base_model_entity import BaseModelEntity
from .pit_table import PitTable


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
    pitTables: Optional[List[PitTable]] = None

    @model_validator(mode="before")
    @classmethod
    def parse_embedded_resources(cls, data: Any) -> Any:
        """Extract embedded resources (pitTables, satellites, etc.) from _embedded."""
        if not isinstance(data, dict):
            return data

        result = data.copy()
        result["pitTables"] = parse_embedded_resource(result, "pitTables")
        return result
