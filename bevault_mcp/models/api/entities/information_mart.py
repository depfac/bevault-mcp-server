"""Information mart entity model."""
from typing import Any, List, Literal, Optional

from pydantic import Field, model_validator

from ..base import BeVaultEntity


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
    def parse_embedded_data(cls, data: Any) -> Any:
        """Parse columns from nested _embedded structure."""
        if not isinstance(data, dict):
            return data

        result = data.copy()

        # Parse columns from nested _embedded structure
        # Structure: _embedded.columns._embedded.columns
        columns = []
        if "_embedded" in result:
            embedded = result["_embedded"]
            if "columns" in embedded:
                columns_embedded = embedded["columns"]
                if isinstance(columns_embedded, dict) and "_embedded" in columns_embedded:
                    columns_list = columns_embedded["_embedded"].get("columns", [])
                    if isinstance(columns_list, list):
                        columns = columns_list

        result["columns"] = columns

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
    def parse_embedded_data(cls, data: Any) -> Any:
        """Parse scripts from nested _embedded structure."""
        if not isinstance(data, dict):
            return data

        result = data.copy()

        # Parse scripts from nested _embedded structure
        # Structure: _embedded.informationMartScripts
        scripts = []
        if "_embedded" in result:
            embedded = result["_embedded"]
            if "informationMartScripts" in embedded:
                scripts_list = embedded["informationMartScripts"]
                if isinstance(scripts_list, list):
                    scripts = scripts_list

        result["scripts"] = scripts

        return result
