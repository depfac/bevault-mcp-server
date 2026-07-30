"""Tests for entity response parsing of businessName."""

from bevault_mcp.metavault.models.api.entities.hub import Hub
from bevault_mcp.metavault.models.api.entities.link import Link
from bevault_mcp.metavault.models.api.entities.satellite import Satellite
from bevault_mcp.metavault.models.response.search import (
    OptimizedHub,
    OptimizedLink,
    OptimizedSatellite,
)


def test_hub_entity_parses_business_name() -> None:
    hub = Hub.model_validate(
        {
            "id": "h1",
            "name": "Customer",
            "entityType": "Hub",
            "businessName": "Customer Account",
        }
    )
    assert hub.businessName == "Customer Account"


def test_link_entity_parses_business_name() -> None:
    link = Link.model_validate(
        {
            "id": "l1",
            "name": "CustOrder",
            "entityType": "Link",
            "businessName": "Customer Order",
        }
    )
    assert link.businessName == "Customer Order"


def test_satellite_entity_parses_business_name_and_keeps_display_name() -> None:
    satellite = Satellite.model_validate(
        {
            "id": "s1",
            "name": "Customer_Details",
            "entityType": "Satellite",
            "businessName": "Customer Details",
            "displayName": "Legacy Display",
        }
    )
    assert satellite.businessName == "Customer Details"
    assert satellite.displayName == "Legacy Display"


def test_hub_entity_allows_missing_business_name() -> None:
    hub = Hub.model_validate({"id": "h1", "name": "Customer", "entityType": "Hub"})
    assert hub.businessName is None


def test_optimized_search_models_include_business_name() -> None:
    assert (
        OptimizedHub(
            id="h1", name="Customer", businessName="Customer Account"
        ).businessName
        == "Customer Account"
    )
    assert (
        OptimizedLink(
            id="l1", name="CustOrder", businessName="Customer Order"
        ).businessName
        == "Customer Order"
    )
    assert (
        OptimizedSatellite(
            id="s1", name="Customer_Details", businessName="Customer Details"
        ).businessName
        == "Customer Details"
    )
