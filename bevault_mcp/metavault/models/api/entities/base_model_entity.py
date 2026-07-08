"""Base model entity with common fields."""

from typing import Any, Dict, Optional

from ..base import BeVaultEntity


class BaseModelEntity(BeVaultEntity):
    """Base class for all model entities (Hub, Link, Satellite, ReferenceTable)."""

    id: str
    name: str
    entityType: str  # Overridden in subclasses with Literal types
    tableName: Optional[str] = None
    businessDescription: Optional[str] = None
    technicalDescription: Optional[str] = None
    _embedded: Optional[Dict[str, Any]] = None
