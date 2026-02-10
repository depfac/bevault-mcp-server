"""Information mart creation request models."""

from typing import List, Optional

from pydantic import Field

from ..api.base import BeVaultRequest


class CreateInformationMartRequest(BeVaultRequest):
    """Request model for creating an information mart."""

    name: str
    databaseSchema: str = Field(alias="schema")
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    prefix: Optional[str] = None
    snapshotId: Optional[str] = None


class CreateInformationMartScriptRequest(BeVaultRequest):
    """Request model for creating an information mart script."""

    name: str
    order: int
    timeout: int = 60
    columns: List = Field(default_factory=list)
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    tableName: Optional[str] = None


class UpdateSourceColumnRequest(BeVaultRequest):
    """Request model for updating a source column reference."""

    entityType: str
    entityName: str
    columnName: str
    id: Optional[str] = None
    informationMartId: Optional[str] = None
    informationMartScriptId: Optional[str] = None
    informationMartScriptColumnId: Optional[str] = None


class UpdateInformationMartScriptColumnRequest(BeVaultRequest):
    """Request model for updating an information mart script column."""

    name: str
    id: Optional[str] = None
    informationMartId: Optional[str] = None
    informationMartScriptId: Optional[str] = None
    comment: Optional[str] = None
    softRule: Optional[str] = None
    sourceColumns: List[UpdateSourceColumnRequest] = Field(default_factory=list)


class UpdateInformationMartScriptRequest(BeVaultRequest):
    """Request model for updating an information mart script metadata (excluding code)."""

    name: str
    id: str
    informationMartId: str
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    tableName: Optional[str] = None
    typeTag: Optional[str] = None
    order: Optional[int] = None
    timeout: Optional[int] = None
    code: Optional[str] = None
    columns: List[UpdateInformationMartScriptColumnRequest] = Field(
        default_factory=list
    )
