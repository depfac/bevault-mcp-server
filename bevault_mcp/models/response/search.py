"""Optimized search response models for MCP server (token-efficient)."""
from typing import Literal, Optional, Union

from pydantic import BaseModel


class OptimizedHub(BaseModel):
    """Optimized hub entity for search response."""

    id: str
    name: str
    entityType: Literal["Hub"] = "Hub"
    tableName: Optional[str] = None
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    satelliteCount: Optional[int] = None
    dependentLinkCount: Optional[int] = None
    businessKeyLength: Optional[int] = None  # Extracted from businessKey.length


class OptimizedLink(BaseModel):
    """Optimized link entity for search response."""

    id: str
    name: str
    entityType: Literal["Link"] = "Link"
    tableName: Optional[str] = None
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    linkType: Optional[str] = None
    dependentLinkCount: Optional[int] = None


class OptimizedSatellite(BaseModel):
    """Optimized satellite entity for search response."""

    id: str
    name: str
    entityType: Literal["Satellite"] = "Satellite"
    tableName: Optional[str] = None
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    parentType: Optional[str] = None
    parentName: Optional[str] = None  # Replaces parentId - fetched from parent entity
    isMultiActive: Optional[bool] = None
    mappingCount: Optional[int] = None


class OptimizedReferenceTable(BaseModel):
    """Optimized reference table entity for search response."""

    id: str
    name: str
    entityType: Literal["ReferenceTable"] = "ReferenceTable"
    tableName: Optional[str] = None
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    mappingCount: Optional[int] = None


OptimizedEntity = Union[OptimizedHub, OptimizedLink, OptimizedSatellite, OptimizedReferenceTable]


class PagingInfo(BaseModel):
    """Paging information for search results."""

    index: int
    limit: int
    total: int


class OptimizedSearchResponse(BaseModel):
    """Optimized search response with paging and entities."""

    paging: PagingInfo
    entities: list[OptimizedEntity]

