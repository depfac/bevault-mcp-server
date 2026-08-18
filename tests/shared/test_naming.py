"""Tests for technical and business name validation helpers."""

import pytest

from bevault_mcp.shared.utils import (
    HUB_TECHNICAL_NAME_MAX_LENGTH,
    LINK_TECHNICAL_NAME_MAX_LENGTH,
    SATELLITE_TECHNICAL_NAME_MAX_LENGTH,
    validate_business_name,
    validate_technical_name,
)


@pytest.mark.parametrize(
    ("value", "max_length"),
    [
        ("Customer", HUB_TECHNICAL_NAME_MAX_LENGTH),
        ("a" * HUB_TECHNICAL_NAME_MAX_LENGTH, HUB_TECHNICAL_NAME_MAX_LENGTH),
        ("Cust_01", LINK_TECHNICAL_NAME_MAX_LENGTH),
        ("a" * LINK_TECHNICAL_NAME_MAX_LENGTH, LINK_TECHNICAL_NAME_MAX_LENGTH),
        ("Details", SATELLITE_TECHNICAL_NAME_MAX_LENGTH),
        (
            "a" * SATELLITE_TECHNICAL_NAME_MAX_LENGTH,
            SATELLITE_TECHNICAL_NAME_MAX_LENGTH,
        ),
    ],
)
def test_validate_technical_name_accepts_valid_values(
    value: str, max_length: int
) -> None:
    assert (
        validate_technical_name(value, entity_label="Entity", max_length=max_length)
        == value
    )


@pytest.mark.parametrize(
    "value",
    ["", "   ", "Cust-omer", "Cust omer", "Cust.omer", "Café"],
)
def test_validate_technical_name_rejects_invalid_characters(value: str) -> None:
    with pytest.raises(ValueError, match="technical name"):
        validate_technical_name(
            value, entity_label="Hub", max_length=HUB_TECHNICAL_NAME_MAX_LENGTH
        )


@pytest.mark.parametrize(
    ("max_length", "entity_label"),
    [
        (HUB_TECHNICAL_NAME_MAX_LENGTH, "Hub"),
        (LINK_TECHNICAL_NAME_MAX_LENGTH, "Link"),
        (SATELLITE_TECHNICAL_NAME_MAX_LENGTH, "Satellite"),
    ],
)
def test_validate_technical_name_rejects_over_max_length(
    max_length: int, entity_label: str
) -> None:
    with pytest.raises(ValueError, match=f"at most {max_length}"):
        validate_technical_name(
            "a" * (max_length + 1), entity_label=entity_label, max_length=max_length
        )


def test_validate_business_name_accepts_unrestricted_values() -> None:
    value = "Customer Account — Primary (EU/FR) 顧客 " + ("x" * 200)
    assert validate_business_name(value) == value


@pytest.mark.parametrize("value", ["", "   "])
def test_validate_business_name_rejects_empty(value: str) -> None:
    with pytest.raises(ValueError, match="must be non-empty"):
        validate_business_name(value)
