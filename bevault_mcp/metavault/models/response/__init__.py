"""Optimized response models for MCP tools (token-efficient)."""

from .search import (
    OptimizedEntity,
    OptimizedHub,
    OptimizedLink,
    OptimizedReferenceTable,
    OptimizedSatellite,
    OptimizedSearchResponse,
    PagingInfo,
)
from .source_systems import (
    OptimizedDataPackage,
    OptimizedSourceSystem,
    OptimizedSourceSystemsResponse,
    StagingTableInfo,
)
from .information_marts import (
    OptimizedInformationMart,
    OptimizedInformationMartScript,
    OptimizedInformationMartsResponse,
)

__all__ = [
    "OptimizedDataPackage",
    "OptimizedEntity",
    "OptimizedHub",
    "OptimizedLink",
    "OptimizedReferenceTable",
    "OptimizedSatellite",
    "OptimizedSearchResponse",
    "OptimizedInformationMart",
    "OptimizedInformationMartScript",
    "OptimizedInformationMartsResponse",
    "OptimizedSourceSystem",
    "OptimizedSourceSystemsResponse",
    "PagingInfo",
    "StagingTableInfo",
]
