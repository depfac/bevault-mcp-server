"""Reference table entity model."""
from typing import Literal, Optional

from .base_model_entity import BaseModelEntity


class ReferenceTable(BaseModelEntity):
    """Reference table entity with reference table-specific fields."""

    entityType: Literal["ReferenceTable"] = "ReferenceTable"
    mappingCount: Optional[int] = None

