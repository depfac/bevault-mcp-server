"""Sentry initialization with environment variable configuration."""

import os
from typing import Any

from dotenv import load_dotenv


def _parse_bool(value: str | None) -> bool:
    """Parse a string as boolean. Accepts 1, true, yes (case-insensitive)."""
    if value is None:
        return False
    return value.strip().lower() in ("1", "true", "yes")


def _parse_default_tags() -> dict[str, str]:
    """Extract default tags from SENTRY_DEFAULTTAGS__[key]=[value] env vars."""
    prefix = "SENTRY_DEFAULTTAGS__"
    tags: dict[str, str] = {}
    for key, value in os.environ.items():
        if key.upper().startswith(prefix.upper()):
            tag_key = key[len(prefix) :].strip()
            if tag_key:
                tags[tag_key] = value
    return tags


def init_sentry() -> None:
    """
    Initialize Sentry SDK when SENTRY_DSN is set.

    Configuration via environment variables:
    - SENTRY_DSN: Required for activation; if unset, Sentry is disabled
    - SENTRY_ENVIRONMENT: Environment name (default: production)
    - SENTRY_TRACES_SAMPLE_RATE: Fraction 0.0-1.0 (default: 1.0)
    - SENTRY_SEND_DEFAULT_PII: Send tool inputs/outputs (default: false)
    - SENTRY_DEBUG: Enable debug logging (default: false)
    - SENTRY_INCLUDE_PROMPTS: Include prompt/tool data in spans (default: true)
    - SENTRY_SERVER_NAME: Server instance identifier
    - SENTRY_DEFAULTTAGS__[key]: Default tags, e.g. SENTRY_DEFAULTTAGS__service=bevault-mcp
    """
    load_dotenv()

    dsn = os.getenv("SENTRY_DSN", "").strip()
    if not dsn:
        return

    import sentry_sdk
    from sentry_sdk.integrations.mcp import MCPIntegration

    traces_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))
    send_default_pii = _parse_bool(os.getenv("SENTRY_SEND_DEFAULT_PII", "false"))
    include_prompts = _parse_bool(os.getenv("SENTRY_INCLUDE_PROMPTS", "true"))

    init_options: dict[str, Any] = {
        "dsn": dsn,
        "environment": os.getenv("SENTRY_ENVIRONMENT", "production"),
        "traces_sample_rate": traces_sample_rate,
        "send_default_pii": send_default_pii,
        "debug": _parse_bool(os.getenv("SENTRY_DEBUG", "false")),
        "integrations": [MCPIntegration(include_prompts=include_prompts)],
    }

    server_name = os.getenv("SENTRY_SERVER_NAME", "").strip()
    if server_name:
        init_options["server_name"] = server_name

    sentry_sdk.init(**init_options)

    # Apply default tags from SENTRY_DEFAULTTAGS__[key]=[value]
    # Use global scope so tags apply to ALL events (isolation scope is request-specific)
    default_tags = _parse_default_tags()
    if default_tags:
        global_scope = sentry_sdk.get_global_scope()
        global_scope.set_tags(default_tags)
