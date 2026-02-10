"""Satellite entity model."""

from typing import Any, List, Literal, Optional, Union

from pydantic import Field, model_validator

from ..base import BeVaultEntity
from .base_model_entity import BaseModelEntity
from .hub import Hub
from .link import Link


class SatelliteColumn(BeVaultEntity):
    """Satellite column entity."""

    id: str
    columnName: str
    dataType: str
    typeFullName: str
    order: int
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    businessName: Optional[str] = None
    description: Optional[str] = None


class Satellite(BaseModelEntity):
    """Satellite entity with satellite-specific fields."""

    entityType: Literal["Satellite"] = "Satellite"
    parentType: Optional[str] = None
    parentId: Optional[str] = None
    isMultiActive: Optional[bool] = None
    mappingCount: Optional[int] = None
    displayName: Optional[str] = None
    subSequenceColumn: Optional[SatelliteColumn] = None
    columns: List[SatelliteColumn] = Field(default_factory=list)
    parent: Optional[Union["Hub", "Link"]] = None

    @model_validator(mode="before")
    @classmethod
    def parse_embedded_data(cls, data: Any) -> Any:
        """Parse columns and parent from _embedded structure."""
        if not isinstance(data, dict):
            return data

        result = data.copy()

        # Parse columns and parent from _embedded structure
        columns = []
        parent = None
        if "_embedded" in result:
            embedded = result.get("_embedded", {})
            if "columns" in embedded:
                columns_list = embedded.get("columns", [])
                if isinstance(columns_list, list):
                    columns = columns_list
            if "parent" in embedded:
                parent = embedded.get("parent")

        result["columns"] = columns
        result["parent"] = parent

        return result
