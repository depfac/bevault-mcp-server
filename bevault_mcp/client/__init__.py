"""Main beVault client."""
import httpx

from ..config import Settings
from .base import BaseClient
from .information_marts import InformationMartsClient
from .mappings import MappingsClient
from .model import ModelClient
from .projects import ProjectsClient
from .source_systems import SourceSystemsClient


class BeVaultClient:
    """Main client for beVault API - facade for all resource clients."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        http_client = httpx.Client(
            base_url=settings.bevault_base_url,
            timeout=settings.request_timeout_seconds,
            headers={"Accept": "application/json"},
        )

        # Initialize resource clients
        self.projects = ProjectsClient(settings, http_client)
        self.model = ModelClient(settings, http_client)
        self.source_systems = SourceSystemsClient(settings, http_client)
        self.mappings = MappingsClient(settings, http_client)
        self.information_marts = InformationMartsClient(settings, http_client)

        # Keep reference for cleanup
        self._client = http_client

    def __enter__(self) -> "BeVaultClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001, D401
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

