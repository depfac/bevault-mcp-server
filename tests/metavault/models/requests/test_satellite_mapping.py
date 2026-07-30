"""Tests for satellite mapping request payload."""

import pytest
from pydantic import ValidationError

from bevault_mcp.metavault.models.requests.satellite_mapping import (
    CreateSatelliteMappingRequest,
)
from bevault_mcp.shared.utils import SATELLITE_TECHNICAL_NAME_MAX_LENGTH


def test_satellite_mapping_request_serializes_business_name() -> None:
    request = CreateSatelliteMappingRequest(
        satelliteName="Details",
        satelliteBusinessName="Customer Details — Primary",
        satelliteColumns=["http://example/columns/c1"],
        stagingTable="http://example/tables/t1",
    )
    payload = request.model_dump(mode="json", exclude_none=True)
    assert payload["satelliteName"] == "Details"
    assert payload["satelliteBusinessName"] == "Customer Details — Primary"
    assert payload["satelliteColumns"] == ["http://example/columns/c1"]
    assert payload["stagingTable"] == "http://example/tables/t1"
    assert payload["isMultiActive"] is False
    assert "subSequenceColumn" not in payload


def test_satellite_mapping_request_includes_optional_sub_sequence() -> None:
    request = CreateSatelliteMappingRequest(
        satelliteName="Details",
        satelliteBusinessName="Details",
        satelliteColumns=[],
        stagingTable="http://example/tables/t1",
        isMultiActive=True,
        subSequenceColumn="http://example/columns/seq",
    )
    payload = request.model_dump(mode="json", exclude_none=True)
    assert payload["subSequenceColumn"] == "http://example/columns/seq"
    assert payload["isMultiActive"] is True


def test_satellite_mapping_request_rejects_invalid_technical_name() -> None:
    with pytest.raises(ValidationError, match="technical name"):
        CreateSatelliteMappingRequest(
            satelliteName="Bad-Name",
            satelliteBusinessName="Details",
            satelliteColumns=[],
            stagingTable="http://example/tables/t1",
        )


def test_satellite_mapping_request_accepts_max_technical_name_length() -> None:
    name = "a" * SATELLITE_TECHNICAL_NAME_MAX_LENGTH
    request = CreateSatelliteMappingRequest(
        satelliteName=name,
        satelliteBusinessName="Details",
        satelliteColumns=[],
        stagingTable="http://example/tables/t1",
    )
    assert request.satelliteName == name


def test_satellite_mapping_request_rejects_over_max_technical_name() -> None:
    with pytest.raises(ValidationError, match="at most 20"):
        CreateSatelliteMappingRequest(
            satelliteName="a" * (SATELLITE_TECHNICAL_NAME_MAX_LENGTH + 1),
            satelliteBusinessName="Details",
            satelliteColumns=[],
            stagingTable="http://example/tables/t1",
        )


def test_satellite_mapping_request_rejects_empty_business_name() -> None:
    with pytest.raises(ValidationError, match="satelliteBusinessName"):
        CreateSatelliteMappingRequest(
            satelliteName="Details",
            satelliteBusinessName="   ",
            satelliteColumns=[],
            stagingTable="http://example/tables/t1",
        )


def test_satellite_mapping_request_requires_business_name() -> None:
    with pytest.raises(ValidationError):
        CreateSatelliteMappingRequest(  # type: ignore[call-arg]
            satelliteName="Details",
            satelliteColumns=[],
            stagingTable="http://example/tables/t1",
        )
