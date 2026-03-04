import os
from dataclasses import dataclass

from dotenv import load_dotenv

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
    bevault_base_url: str
    request_timeout_seconds: float

    @staticmethod
    def from_env() -> "Settings":
        # Load .env if present
        load_dotenv()

        base_url = os.getenv("BEVAULT_BASE_URL", "").rstrip("/")
        timeout = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

        if not base_url:
            raise ValueError("BEVAULT_BASE_URL is required")

        return Settings(
            bevault_base_url=base_url,
            request_timeout_seconds=timeout,
        )



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