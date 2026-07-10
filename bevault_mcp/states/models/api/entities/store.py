"""Store entity models."""

from ..base import StatesEntity


class StoreSource(StatesEntity):
    """Source metadata for locally configured stores."""

    workerServiceEnvironmentName: str | None = None
    workerServiceCreateDate: str | None = None


class StoreListItem(StatesEntity):
    """Store item returned by the list endpoint."""

    name: str
    type: str
    id: str | None = None
    enableHealthCheck: bool = False
    customStore: bool = False
    healthCheckDelaySeconds: int | None = None
    businessDescription: str | None = None
    technicalDescription: str | None = None
    config: dict | None = None
    source: StoreSource | None = None
