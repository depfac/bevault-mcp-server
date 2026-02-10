import os
from dataclasses import dataclass

from dotenv import load_dotenv


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
