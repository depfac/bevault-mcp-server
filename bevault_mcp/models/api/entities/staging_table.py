"""Staging table entity models."""
from typing import List, Optional

from pydantic import BaseModel, Field

from ..base import BeVaultEntity


class BaseType(BaseModel):
    """Base type information for a column (source type)."""

    isText: bool
    isBinary: bool
    type: str
    dataType: str
    length: Optional[int] = None  # For String type
    scale: Optional[int] = None  # For VarNumeric type
    precision: Optional[int] = None  # For VarNumeric type
    autoIncrement: bool


class StagingTableColumn(BaseModel):
    """Staging table column entity (response model)."""

    id: str
    name: str
    dataType: str  # Target type (final type after casting if hard rule exists)
    length: Optional[int] = None  # For String target type
    scale: Optional[int] = None  # For VarNumeric target type
    precision: Optional[int] = None  # For VarNumeric target type
    baseType: BaseType  # Source type (original type before casting)
    nullable: bool
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None
    businessName: Optional[str] = None
    primaryKey: bool
    typeFullName: str
    hardRuleDefinition: Optional[str] = None
    # Note: hardRuleDefinition contains SQL code for type casting (e.g., "{{contract_number}}::int"),
    # where column names are referenced using {{column_name}} syntax


class Columns(BaseModel):
    """Container for embedded columns."""

    columns: List[StagingTableColumn] = Field(default_factory=list)


class StagingTable(BeVaultEntity):
    """Staging table entity."""

    id: str
    tableName: str
    targetTableName: str
    targetSchemaName: str
    dataPackageId: str
    query: str
    queryType: str
    isQueryBased: bool
    embedded: Optional[Columns] = Field(None, alias="_embedded")

    @property
    def _embedded(self) -> Optional[Columns]:
        """Access _embedded via property for backward compatibility."""
        return self.embedded

    @property
    def columns(self) -> List[StagingTableColumn]:
        """Convenience property to access columns from _embedded."""
        if self.embedded:
            return self.embedded.columns
        return []

