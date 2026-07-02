"""Base classes for States API models."""

from pydantic import BaseModel, ConfigDict


class StatesEntity(BaseModel):
    """Base class for States API entity models."""

    model_config = ConfigDict(extra="ignore")
