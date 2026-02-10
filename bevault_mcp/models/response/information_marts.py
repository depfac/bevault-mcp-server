"""Optimized information marts response models for MCP server (token-efficient)."""

from typing import List, Optional

from pydantic import BaseModel, Field

from .search import PagingInfo


class OptimizedInformationMartScript(BaseModel):
    """Optimized information mart script for search response."""

    id: str
    name: str
    order: int
    businessDescription: Optional[str] = None


class OptimizedInformationMart(BaseModel):
    """Optimized information mart entity for search response."""

    id: str
    name: str
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    schema_: Optional[str] = Field(default=None, alias="schema")
    prefix: Optional[str] = None
    scriptsCount: Optional[int] = None
    snapshotId: Optional[str] = None
    scripts: List[OptimizedInformationMartScript] = []


class OptimizedInformationMartsResponse(BaseModel):
    """Optimized information marts search response with paging and information marts."""

    paging: PagingInfo
    informationMarts: List[OptimizedInformationMart]
