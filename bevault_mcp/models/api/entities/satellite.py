"""Satellite entity model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Literal, Optional, Union

from pydantic import model_validator

from ..base import BeVaultEntity
from ..embedded import parse_embedded_resource, parse_embedded_single
from .base_model_entity import BaseModelEntity

if TYPE_CHECKING:
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
    columns: Optional[List[SatelliteColumn]] = None
    parent: Optional[Union["Hub", "Link"]] = None

    @model_validator(mode="before")
    @classmethod
    def parse_embedded_resources(cls, data: Any) -> Any:
        """Extract embedded resources (columns, parent) from _embedded."""
        if not isinstance(data, dict):
            return data

        result = data.copy()
        columns = parse_embedded_resource(result, "columns")
        result["columns"] = columns if columns else None
        result["parent"] = parse_embedded_single(result, "parent")

        return result
