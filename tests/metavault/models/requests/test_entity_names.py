"""Tests for hub and link request models with business names."""

import pytest
from pydantic import ValidationError

from bevault_mcp.metavault.models.requests.hub import CreateHubRequest
from bevault_mcp.metavault.models.requests.link import CreateLinkRequest
from bevault_mcp.shared.utils import (
    HUB_TECHNICAL_NAME_MAX_LENGTH,
    LINK_TECHNICAL_NAME_MAX_LENGTH,
)


def test_create_hub_request_requires_business_name() -> None:
    with pytest.raises(ValidationError):
        CreateHubRequest(name="Customer")  # type: ignore[call-arg]


def test_create_hub_request_serializes_business_name() -> None:
    request = CreateHubRequest(
        name="Customer",
        businessName="Customer Account — Primary",
    )
    payload = request.model_dump(mode="json", exclude_none=True)
    assert payload["name"] == "Customer"
    assert payload["businessName"] == "Customer Account — Primary"


def test_create_hub_request_rejects_invalid_technical_name() -> None:
    with pytest.raises(ValidationError, match="technical name"):
        CreateHubRequest(name="Cust-omer", businessName="Customer")


def test_create_hub_request_accepts_max_technical_name_length() -> None:
    name = "a" * HUB_TECHNICAL_NAME_MAX_LENGTH
    request = CreateHubRequest(name=name, businessName="Customer")
    assert request.name == name


def test_create_hub_request_rejects_over_max_technical_name_length() -> None:
    with pytest.raises(ValidationError, match="at most 25"):
        CreateHubRequest(
            name="a" * (HUB_TECHNICAL_NAME_MAX_LENGTH + 1),
            businessName="Customer",
        )


def test_create_link_request_requires_business_name() -> None:
    with pytest.raises(ValidationError):
        CreateLinkRequest(name="CustOrder")  # type: ignore[call-arg]


def test_create_link_request_serializes_business_name() -> None:
    request = CreateLinkRequest(
        name="CustOrder",
        businessName="Customer to Order Relationship",
    )
    payload = request.model_dump(mode="json", exclude_none=True)
    assert payload["name"] == "CustOrder"
    assert payload["businessName"] == "Customer to Order Relationship"


def test_create_link_request_accepts_max_technical_name_length() -> None:
    name = "a" * LINK_TECHNICAL_NAME_MAX_LENGTH
    request = CreateLinkRequest(name=name, businessName="Link Business")
    assert request.name == name


def test_create_link_request_rejects_over_max_technical_name_length() -> None:
    with pytest.raises(ValidationError, match="at most 35"):
        CreateLinkRequest(
            name="a" * (LINK_TECHNICAL_NAME_MAX_LENGTH + 1),
            businessName="Link Business",
        )
