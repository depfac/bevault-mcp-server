import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("true", "1", "yes")


@dataclass
class OidcConfig:
    config_url: str
    client_id: str
    client_secret: str
    base_url: str
    audience: str | None = None
    redirect_path: str | None = None
    required_scopes: list[str] | None = None


@dataclass
class Settings:
    metavault_enabled: bool
    states_enabled: bool
    bevault_base_url: str | None
    states_base_url: str | None
    request_timeout_seconds: float

    @staticmethod
    def from_env() -> "Settings":
        load_dotenv()

        metavault_enabled = _env_bool("METAVAULT_ENABLED", default=True)
        states_enabled = _env_bool("STATES_ENABLED", default=False)
        timeout = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

        bevault_base_url = os.getenv("BEVAULT_BASE_URL", "").rstrip("/") or None
        states_base_url = os.getenv("STATES_BASE_URL", "").rstrip("/") or None

        settings = Settings(
            metavault_enabled=metavault_enabled,
            states_enabled=states_enabled,
            bevault_base_url=bevault_base_url,
            states_base_url=states_base_url,
            request_timeout_seconds=timeout,
        )
        settings._validate()
        return settings

    def _validate(self) -> None:
        if not self.metavault_enabled and not self.states_enabled:
            raise ValueError(
                "At least one module must be enabled "
                "(METAVAULT_ENABLED or STATES_ENABLED)"
            )

        if self.metavault_enabled and not self.bevault_base_url:
            raise ValueError("BEVAULT_BASE_URL is required when METAVAULT_ENABLED=true")

        if self.states_enabled and not self.states_base_url:
            raise ValueError("STATES_BASE_URL is required when STATES_ENABLED=true")

    def require_bevault_base_url(self) -> str:
        """Return BEVAULT_BASE_URL or raise if unset."""
        if self.bevault_base_url is None:
            raise ValueError("BEVAULT_BASE_URL is required")
        return self.bevault_base_url

    def get_oidc_config(self) -> OidcConfig | None:
        """Return OIDC config if all required env vars are set."""
        config_url = os.getenv("OIDC_CONFIG_URL", "").strip()
        client_id = os.getenv("OIDC_CLIENT_ID", "").strip()
        client_secret = os.getenv("OIDC_CLIENT_SECRET", "").strip()
        base_url = os.getenv("OIDC_BASE_URL", "").strip()

        if not all([config_url, client_id, client_secret, base_url]):
            return None

        audience = os.getenv("OIDC_AUDIENCE", "").strip() or None
        redirect_path = os.getenv("OIDC_REDIRECT_PATH", "").strip() or None
        required_scopes_raw = os.getenv("OIDC_REQUIRED_SCOPES", "").strip()
        required_scopes = (
            [scope.strip() for scope in required_scopes_raw.split(",") if scope.strip()]
            if required_scopes_raw
            else None
        )

        return OidcConfig(
            config_url=config_url,
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            audience=audience,
            redirect_path=redirect_path,
            required_scopes=required_scopes,
        )
