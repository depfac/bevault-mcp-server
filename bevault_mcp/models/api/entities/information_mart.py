"""Information mart entity model."""

from typing import Any, List, Literal, Optional

from pydantic import Field, model_validator

from ..base import BeVaultEntity
from ..embedded import parse_embedded_resource


class SourceColumn(BeVaultEntity):
    """Source column reference entity for information mart script columns."""

    id: str
    entityType: str
    entityName: str
    columnName: str
    informationMartId: Optional[str] = None
    informationMartScriptId: Optional[str] = None
    informationMartScriptColumnId: Optional[str] = None


class InformationMartScriptColumn(BeVaultEntity):
    """Information mart script column entity."""

    id: str
    name: str
    comment: Optional[str] = None
    softRule: Optional[str] = None
    informationMartId: Optional[str] = None
    informationMartScriptId: Optional[str] = None
    sourceColumns: List[SourceColumn] = Field(default_factory=list)


class InformationMartScript(BeVaultEntity):
    """Information mart script entity."""

    id: str
    name: str
    informationMartId: str
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    tableName: Optional[str] = None
    typeTag: Optional[str] = None
    order: int = 0
    timeout: int = 0
    code: Optional[str] = None
    columns: List[InformationMartScriptColumn] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def parse_embedded_resources(cls, data: Any) -> Any:
        """Extract embedded resources (columns) from _embedded."""
        if not isinstance(data, dict):
            return data

        result = data.copy()
        result["columns"] = parse_embedded_resource(result, "columns")

        return result


class InformationMart(BeVaultEntity):
    """Information mart entity."""

    id: str
    name: str
    entityType: Literal["InformationMart"] = "InformationMart"
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    schema_: Optional[str] = Field(default=None, alias="schema")
    prefix: Optional[str] = None
    scriptsCount: Optional[int] = None
    snapshotId: Optional[str] = None
    scripts: List[InformationMartScript] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def parse_embedded_resources(cls, data: Any) -> Any:
        """Extract embedded resources (scripts) from _embedded."""
        if not isinstance(data, dict):
            return data

        result = data.copy()
        result["scripts"] = parse_embedded_resource(
            result, "informationMartScripts", result_key="informationMartScripts"
        )

        return result
