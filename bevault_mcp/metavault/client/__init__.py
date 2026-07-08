"""MetaVault client facade."""

import httpx

from bevault_mcp.config import Settings

from .base import BaseClient as BaseClient
from .information_marts import InformationMartsClient
from .mappings import MappingsClient
from .model import ModelClient
from .projects import ProjectsClient
from .source_systems import SourceSystemsClient

__all__ = ["MetavaultClient", "BaseClient"]


class MetavaultClient:
    """Facade for the beVault MetaVault API resource clients."""

    def __init__(self, settings: Settings) -> None:
        if not settings.bevault_base_url:
            raise ValueError("bevault_base_url is required for MetavaultClient")

        self._settings = settings
        http_client = httpx.Client(
            base_url=settings.require_bevault_base_url(),
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

    def __enter__(self) -> "MetavaultClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001, D401
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()
