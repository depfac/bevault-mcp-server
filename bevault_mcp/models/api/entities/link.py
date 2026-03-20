"""Link entity model."""

from typing import Any, List, Literal, Optional

from pydantic import Field, model_validator

from ..base import BeVaultEntity
from ..embedded import parse_embedded_resource
from .base_model_entity import BaseModelEntity
from .pit_table import PitTable


class HubReference(BeVaultEntity):
    """Hub reference entity for links."""

    id: str
    columnName: str
    order: int
    hubId: str
    linkId: str


class DependentChildColumn(BeVaultEntity):
    """Dependent child column entity for links."""

    id: str
    columnName: str
    dataType: str
    typeFullName: str


class DataColumn(BeVaultEntity):
    """Data column entity for links."""

    id: str
    columnName: str
    dataType: str
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    typeFullName: str


class Link(BaseModelEntity):
    """Link entity with link-specific fields."""

    entityType: Literal["Link"] = "Link"
    linkType: Optional[str] = None
    dependentLinkCount: Optional[int] = None
    hubReferences: List[HubReference] = Field(default_factory=list)
    dependentChildColumns: List[DependentChildColumn] = Field(default_factory=list)
    dataColumns: List[DataColumn] = Field(default_factory=list)
    pitTables: Optional[List[PitTable]] = None

    @model_validator(mode="before")
    @classmethod
    def parse_embedded_resources(cls, data: Any) -> Any:
        """Extract embedded resources (hubReferences, pitTables, satellites, etc.) from _embedded."""
        if not isinstance(data, dict):
            return data

        result = data.copy()
        result["hubReferences"] = parse_embedded_resource(result, "hubReferences")
        result["pitTables"] = parse_embedded_resource(result, "pitTables")

        # dependentChildColumns and dataColumns are already on the Link object
        if "dependentChildColumns" not in result:
            result["dependentChildColumns"] = []
        if "dataColumns" not in result:
            result["dataColumns"] = []

        return result
