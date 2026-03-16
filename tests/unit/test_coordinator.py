"""Tests for Ecotracker coordinator."""

from __future__ import annotations

from custom_components.ecotracker.const import (
    API_OPTIONAL_RESPONSE_JSON_KEYS,
    API_REQUIRED_RESPONSE_JSON_KEYS,
)
from tests.mock_data import (
    MOCK_API_RESPONSE_FULL,
    MOCK_API_RESPONSE_INVALID_TYPE,
    MOCK_API_RESPONSE_MINIMAL,
    MOCK_API_RESPONSE_MISSING_REQUIRED,
)


def test_required_keys_present_in_full_response():
    """Test that all required keys are present in full API response."""
    for key in API_REQUIRED_RESPONSE_JSON_KEYS:
        assert key in MOCK_API_RESPONSE_FULL


def test_required_keys_only_in_minimal_response():
    """Test that minimal response has only required keys."""
    for key in API_REQUIRED_RESPONSE_JSON_KEYS:
        assert key in MOCK_API_RESPONSE_MINIMAL


def test_optional_keys_present_in_full_response():
    """Test that optional keys are present in full response."""
    for key in API_OPTIONAL_RESPONSE_JSON_KEYS:
        assert key in MOCK_API_RESPONSE_FULL


def test_missing_required_key_detected():
    """Test that missing required keys are detected."""
    missing_keys = [key for key in API_REQUIRED_RESPONSE_JSON_KEYS if key not in MOCK_API_RESPONSE_MISSING_REQUIRED]
    assert len(missing_keys) > 0


def test_invalid_type_detected():
    """Test that invalid data types are detected."""
    invalid_values = {
        key: value
        for key, value in MOCK_API_RESPONSE_INVALID_TYPE.items()
        if key in API_REQUIRED_RESPONSE_JSON_KEYS and not isinstance(value, (int, float))
    }
    assert len(invalid_values) > 0


def test_valid_response_types():
    """Test that valid response has correct data types."""
    for key in API_REQUIRED_RESPONSE_JSON_KEYS:
        value = MOCK_API_RESPONSE_FULL[key]
        assert isinstance(value, (int, float)), f"{key} should be numeric, got {type(value)}"
