"""Snapshot entity model."""

from typing import Optional

from ..base import BeVaultEntity


class Snapshot(BeVaultEntity):
    """Snapshot entity."""

    id: str
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
