"""Tests for staging table request models."""

import pytest
from pydantic import ValidationError

from bevault_mcp.metavault.models.requests.staging_table import StagingTableColumn


def test_numeric_column_maps_friendly_type_and_serializes() -> None:
    column = StagingTableColumn(
        name="amount",
        dataType="Numeric",
        precision=18,
        scale=2,
    )
    assert column.dataType == "VarNumeric"
    payload = column.model_dump(mode="json", exclude_none=True)
    assert payload["dataType"] == "VarNumeric"
    assert payload["precision"] == 18
    assert payload["scale"] == 2


def test_varnumeric_column_accepts_api_type() -> None:
    column = StagingTableColumn(
        name="amount",
        dataType="VarNumeric",
        precision=10,
        scale=4,
    )
    assert column.dataType == "VarNumeric"
    assert column.precision == 10
    assert column.scale == 4


def test_numeric_column_requires_precision() -> None:
    with pytest.raises(ValidationError, match="precision is required"):
        StagingTableColumn(
            name="amount",
            dataType="Numeric",
            scale=2,
        )


def test_numeric_column_requires_scale() -> None:
    with pytest.raises(ValidationError, match="scale is required"):
        StagingTableColumn(
            name="amount",
            dataType="VarNumeric",
            precision=18,
        )


def test_string_column_still_requires_length() -> None:
    with pytest.raises(ValidationError, match="length is required"):
        StagingTableColumn(name="label", dataType="Text")


def test_string_column_does_not_require_scale_or_precision() -> None:
    column = StagingTableColumn(name="label", dataType="Text", length=50)
    payload = column.model_dump(mode="json", exclude_none=True)
    assert payload["dataType"] == "String"
    assert payload["length"] == 50
    assert "precision" not in payload
    assert "scale" not in payload


def test_integer_column_does_not_require_numeric_parameters() -> None:
    column = StagingTableColumn(name="count", dataType="Integer")
    assert column.dataType == "Int32"
    payload = column.model_dump(mode="json", exclude_none=True)
    assert "precision" not in payload
    assert "scale" not in payload
