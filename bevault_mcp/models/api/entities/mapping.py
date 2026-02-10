"""Staging table mapping entity models."""

from typing import List, Optional, Union

from pydantic import BaseModel, Field, model_validator


class BusinessKeyMapping(BaseModel):
    """Business key mapping for hub mappings."""

    businessKeyId: str
    columnId: str


class HubReferenceColumnMapping(BaseModel):
    """Hub reference column mapping for link mappings."""

    hubReferenceId: str
    mappingId: str


class DependentChildColumnMapping(BaseModel):
    """Dependent child column mapping for link mappings."""

    dependentChildId: str = Field(alias="linkColumnId")
    stagingTableColumnId: str = Field(alias="tableColumnId")

    model_config = {"populate_by_name": True}


class DataColumnMapping(BaseModel):
    """Data column mapping for link mappings."""

    dataColumnId: str = Field(alias="linkColumnId")
    stagingTableColumnId: str = Field(alias="tableColumnId")

    model_config = {"populate_by_name": True}


class SatelliteColumnMapping(BaseModel):
    """Satellite column mapping for satellite mappings."""

    satelliteColumnId: str
    stagingTableColumnId: str


class BaseMapping(BaseModel):
    """Base mapping entity with common fields."""

    id: str
    name: str
    parentName: str
    mappingType: str
    dataPackageTableId: str
    sourceSystemName: Optional[str] = None
    dataPackageName: Optional[str] = None
    dataPackageTableName: Optional[str] = None


class HubMapping(BaseMapping):
    """Hub mapping entity."""

    mappingType: str = "Hub"
    hubId: str
    isFullLoad: bool
    expectNullBusinessKey: bool
    businessKeyMapping: BusinessKeyMapping


class LinkMapping(BaseMapping):
    """Link mapping entity."""

    mappingType: str = "Link"
    linkId: str
    isFullLoad: bool
    hubReferenceColumnMappings: List[HubReferenceColumnMapping] = Field(
        default_factory=list
    )
    dependentChildColumnMappings: List[DependentChildColumnMapping] = Field(
        default_factory=list
    )
    dataColumnMappings: List[DataColumnMapping] = Field(default_factory=list)


class SatelliteMapping(BaseMapping):
    """Satellite mapping entity."""

    mappingType: str = "Satellite"
    hubId: Optional[str] = None
    linkId: Optional[str] = None
    satelliteId: str
    satelliteParentMappingId: str
    satelliteColumnMappings: List[SatelliteColumnMapping] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_parent_id(self) -> "SatelliteMapping":
        """Ensure at least one of hubId or linkId is present."""
        if not self.hubId and not self.linkId:
            raise ValueError("SatelliteMapping must have either hubId or linkId")
        return self


# Union type for all mapping types
StagingTableMapping = Union[HubMapping, LinkMapping, SatelliteMapping]
