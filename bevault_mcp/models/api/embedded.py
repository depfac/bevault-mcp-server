"""Utilities for parsing HAL embedded resources from beVault API responses."""

from typing import Any, List


def parse_embedded_resource(
    data: dict[str, Any],
    resource_name: str,
    result_key: str | None = None,
) -> List[Any]:
    """
    Extract an embedded resource from a HAL API response.

    Handles both structures:
    - Direct array: _embedded.{resource_name} = [...]
    - Paginated/nested: _embedded.{resource_name}._embedded.{resource_name} = [...]

    Args:
        data: The raw API response dict (with _embedded)
        resource_name: Name of the embedded resource (e.g. "pitTables", "satellites", "hubReferences")
        result_key: Optional key for nested structure (defaults to resource_name)

    Returns:
        List of resource items (raw dicts). Empty list if not found.
    """
    result_key = result_key or resource_name
    if "_embedded" not in data:
        return []

    embedded = data["_embedded"]
    if resource_name not in embedded:
        return []

    resource_data = embedded[resource_name]
    if isinstance(resource_data, list):
        return resource_data

    if (
        isinstance(resource_data, dict)
        and "_embedded" in resource_data
        and result_key in resource_data["_embedded"]
    ):
        items = resource_data["_embedded"][result_key]
        return items if isinstance(items, list) else []

    return []


def strip_columns_from_satellites(satellites: List[Any]) -> List[Any]:
    """
    Remove columns and _embedded from satellite dicts to reduce payload size.

    When satellites are embedded in Hub/Link responses, they may include full
    column definitions. This strips them to avoid huge payloads.
    """
    for item in satellites:
        if isinstance(item, dict):
            item.pop("columns", None)
            item.pop("_embedded", None)
    return satellites


def parse_embedded_resources(
    data: dict[str, Any],
    resource_mappings: dict[str, str],
) -> dict[str, List[Any]]:
    """
    Extract multiple embedded resources from a HAL API response.

    Args:
        data: The raw API response dict (with _embedded)
        resource_mappings: Dict mapping result_key -> resource_name.
            e.g. {"pitTables": "pitTables", "hubReferences": "hubReferences"}
            For nested structures where key differs: {"hubReferences": "hubReferences"}

    Returns:
        Dict mapping result_key to list of items.
    """
    if not isinstance(data, dict):
        return {k: [] for k in resource_mappings}

    result = {}
    for result_key, resource_name in resource_mappings.items():
        result[result_key] = parse_embedded_resource(data, resource_name, result_key)
    return result
