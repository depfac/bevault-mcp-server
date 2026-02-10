"""Link entity model."""

from typing import Any, List, Literal, Optional

from pydantic import Field, model_validator

from ..base import BeVaultEntity
from .base_model_entity import BaseModelEntity


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

    @model_validator(mode="before")
    @classmethod
    def parse_embedded_data(cls, data: Any) -> Any:
        """Parse hub references from nested _embedded structure and extract dependentChildColumns/dataColumns."""
        if not isinstance(data, dict):
            return data

        result = data.copy()

        # Parse hub references from nested _embedded structure
        # Structure: _embedded.hubReferences._embedded.hubReferences
        hub_references = []
        if "_embedded" in result:
            embedded = result["_embedded"]
            if "hubReferences" in embedded:
                hub_refs_embedded = embedded["hubReferences"]
                if (
                    isinstance(hub_refs_embedded, dict)
                    and "_embedded" in hub_refs_embedded
                ):
                    hub_refs_list = hub_refs_embedded["_embedded"].get(
                        "hubReferences", []
                    )
                    if isinstance(hub_refs_list, list):
                        hub_references = hub_refs_list

        result["hubReferences"] = hub_references

        # dependentChildColumns and dataColumns are already on the Link object
        # Just ensure they exist as lists
        if "dependentChildColumns" not in result:
            result["dependentChildColumns"] = []
        if "dataColumns" not in result:
            result["dataColumns"] = []

        return result
