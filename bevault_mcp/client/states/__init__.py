"""Main States API client."""

import httpx

from ...config import Settings
from .activities import ActivitiesClient
from .executions import ExecutionsClient
from .state_machines import StateMachinesClient
from .stores import StoresClient


class StatesClient:
    """Facade for States API resource clients."""

    def __init__(self, settings: Settings) -> None:
        if not settings.states_base_url:
            raise ValueError("states_base_url is required for StatesClient")

        self._settings = settings
        http_client = httpx.Client(
            base_url=settings.states_base_url,
            timeout=settings.request_timeout_seconds,
            headers={"Accept": "application/json"},
        )

        self.state_machines = StateMachinesClient(settings, http_client)
        self.executions = ExecutionsClient(settings, http_client)
        self.activities = ActivitiesClient(settings, http_client)
        self.stores = StoresClient(settings, http_client)
        self._client = http_client

    def __enter__(self) -> "StatesClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001, D401
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()
