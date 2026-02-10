"""Staging table creation request models."""

from typing import Literal, Optional
from pydantic import BaseModel, field_validator, model_validator

from ..api.base import BeVaultRequest


def map_user_type_to_api_type(user_type: str) -> str:
    """
    Map user-friendly type names to API type names.

    Args:
        user_type: User-friendly type name

    Returns:
        API type name
    """
    type_mapping = {
        "DateTime": "DateTime2",
        "Date": "Date",  # No change
        "Text": "String",
        "Boolean": "Boolean",  # No change
        "Integer": "Int32",
        "Numeric": "VarNumeric",
    }
    # If already an API type, return as-is
    if user_type in ["DateTime2", "String", "Int32", "VarNumeric", "Date", "Boolean"]:
        return user_type
    # Otherwise map it
    return type_mapping.get(user_type, user_type)


class StagingTableColumn(BeVaultRequest):
    """Request model for a staging table column definition."""

    name: str
    dataType: str
    businessDescription: Optional[str] = None
    businessName: Optional[str] = None
    technicalDescription: Optional[str] = None
    length: Optional[int] = None

    @field_validator("dataType")
    @classmethod
    def map_data_type(cls, v: str) -> str:
        """Map user-friendly type to API type."""
        return map_user_type_to_api_type(v)

    @model_validator(mode="after")
    def validate_length_for_string(self) -> "StagingTableColumn":
        """Validate that length is provided for String type."""
        if self.dataType == "String" and self.length is None:
            raise ValueError("length is required for String dataType")
        return self


class CreateStagingTableRequest(BeVaultRequest):
    """Request model for creating a staging table."""

    tableName: str
    queryType: Literal["Table", "View"]
    query: str = ""
    columns: Optional[list[StagingTableColumn]] = None

    @model_validator(mode="after")
    def validate_request_structure(self) -> "CreateStagingTableRequest":
        """
        Validate the request structure based on creation type.

        Rules:
        1. Column list: columns provided, queryType="Table"
        2. View: query provided (non-empty), queryType="View"
        3. DDL Table: query provided (non-empty), queryType="Table", no columns
        4. Existing table: query empty, no columns, queryType="Table"
        """
        has_columns = self.columns is not None and len(self.columns) > 0
        has_query = self.query and self.query.strip()

        # Column list creation
        if has_columns:
            if self.queryType != "Table":
                raise ValueError("columns can only be used with queryType='Table'")
            if has_query:
                raise ValueError("columns and query cannot both be provided")
            return self

        # View creation
        if self.queryType == "View":
            if not has_query:
                raise ValueError("query is required when queryType='View'")
            return self

        # DDL Table or Existing table (both use queryType="Table")
        if self.queryType == "Table":
            # Both are valid - DDL table if has_query, existing table if not
            return self

        return self


class BaseTypeRequest(BaseModel):
    """Request model for base type (simplified - backend fills in isText, isBinary, autoIncrement)."""

    type: str  # Source type
    dataType: str  # Source type (same as type)
    length: Optional[int] = None  # For String type

    @field_validator("type", "dataType")
    @classmethod
    def map_data_type(cls, v: str) -> str:
        """Map user-friendly type to API type."""
        return map_user_type_to_api_type(v)


class UpdateStagingTableColumnRequest(BaseModel):
    """Request model for adding or updating a staging table column."""

    id: Optional[str] = None  # Only for update, not for create
    name: str
    dataType: str  # Target type
    baseType: BaseTypeRequest  # Source type (simplified)
    businessDescription: Optional[str] = None
    dataTypeCategory: Optional[str] = None
    showHardRuleData: Optional[bool] = None
    selected: Optional[bool] = None
    hardRuleDefinition: Optional[str] = None
    length: Optional[int] = None  # For String target type

    @field_validator("dataType")
    @classmethod
    def map_data_type(cls, v: str) -> str:
        """Map user-friendly type to API type."""
        return map_user_type_to_api_type(v)
