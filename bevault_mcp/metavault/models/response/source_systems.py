"""Optimized source systems response models for MCP server (token-efficient)."""

from typing import List, Optional

from pydantic import BaseModel

from .search import PagingInfo


class StagingTableInfo(BaseModel):
    """Staging table information with id and name."""

    id: str
    name: str


class OptimizedDataPackage(BaseModel):
    """Optimized data package entity for search response."""

    id: str
    name: str
    deliverySchedule: Optional[str] = None
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None
    refreshType: Optional[str] = None
    formatInfo: Optional[str] = None
    expectedQuality: Optional[str] = None
    stagingTables: List[
        StagingTableInfo
    ] = []  # List of staging tables with id and name


class OptimizedSourceSystem(BaseModel):
    """Optimized source system entity for search response."""

    id: str
    name: str
    code: Optional[str] = None
    version: Optional[str] = None
    qualityType: Optional[str] = None
    dataSteward: Optional[str] = None
    systemAdministrator: Optional[str] = None
    technicalDescription: Optional[str] = None
    businessDescription: Optional[str] = None
    packages: list[OptimizedDataPackage] = []


class OptimizedSourceSystemsResponse(BaseModel):
    """Optimized source systems search response with paging and source systems."""

    paging: PagingInfo
    sourceSystems: list[OptimizedSourceSystem]
