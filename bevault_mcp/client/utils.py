"""Utility functions for client operations."""
import re


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

