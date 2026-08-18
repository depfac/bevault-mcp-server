"""Utility functions for client operations."""

import re

TECHNICAL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

HUB_TECHNICAL_NAME_MAX_LENGTH = 25
LINK_TECHNICAL_NAME_MAX_LENGTH = 35
SATELLITE_TECHNICAL_NAME_MAX_LENGTH = 20


def is_guid(value: str) -> bool:
    """
    Check if a string is a GUID (with or without dashes).

    GUID format:
    - With dashes: 8-4-4-4-12 hex digits (e.g., "01234567-89ab-cdef-0123-456789abcdef")
    - Without dashes: 32 hex digits (e.g., "0123456789abcdef0123456789abcdef")
    """
    if not value:
        return False

    # Remove dashes for checking
    cleaned = value.replace("-", "")

    # Must be exactly 32 hex digits
    return len(cleaned) == 32 and bool(re.match(r"^[0-9a-fA-F]{32}$", cleaned))


def validate_technical_name(value: str, *, entity_label: str, max_length: int) -> str:
    """
    Validate a beVault technical name (database-safe identifier).

    Technical names must be non-empty, at most ``max_length`` characters, and
    contain only ASCII letters, digits, and underscores.
    """
    if not value or not value.strip():
        raise ValueError(f"{entity_label} technical name must be non-empty")
    if len(value) > max_length:
        raise ValueError(
            f"{entity_label} technical name must be at most {max_length} characters "
            f"(got {len(value)})"
        )
    if not TECHNICAL_NAME_PATTERN.fullmatch(value):
        raise ValueError(
            f"{entity_label} technical name must contain only letters, digits, "
            "and underscores"
        )
    return value


def validate_business_name(value: str, *, field_label: str = "businessName") -> str:
    """
    Validate a beVault business name.

    Business names are required and non-empty, with no length or character
    restrictions (beVault 3.12+).
    """
    if not value or not value.strip():
        raise ValueError(f"{field_label} must be non-empty")
    return value
