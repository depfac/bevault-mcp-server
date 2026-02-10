"""Formatted mapping response models."""
from typing import List, Optional

from pydantic import BaseModel


class ColumnMapping(BaseModel):
    """Column mapping representing a source->destination column pair."""

    sourceColumnName: str
    destinationId: str
    destinationType: str  # "businessKey", "hubReference", "dependentChild", "dataColumn", "satelliteColumn"
    destinationColumnName: str


class FormattedMapping(BaseModel):
    """Formatted mapping response model with unified column mappings."""

    id: str
    name: str
    parentName: str
    mappingType: str
    columnMappings: List[ColumnMapping]
    isFullLoad: Optional[bool] = None
