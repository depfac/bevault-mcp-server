"""Model entity representing hubs, links, satellites, etc."""
from typing import Annotated, Union

from pydantic import Discriminator

from .base_model_entity import BaseModelEntity
from .hub import Hub
from .link import Link
from .reference_table import ReferenceTable
from .satellite import Satellite

# Discriminated union for type-safe entity parsing
# The discriminator uses the entityType field to determine which model to use
# BaseModelEntity is excluded as it's abstract - only concrete types are included
ModelEntity = Annotated[
    Union[Hub, Link, Satellite, ReferenceTable],
    Discriminator("entityType"),
]

# For backward compatibility, also export BaseModelEntity
__all__ = ["ModelEntity", "BaseModelEntity"]
