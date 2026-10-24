"""Tests for Ecotracker coordinator."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.ecotracker.const import (
    API_OPTIONAL_RESPONSE_JSON_KEYS,
    API_REQUIRED_RESPONSE_JSON_KEYS,
)
from custom_components.ecotracker.coordinator import InvalidData, fetch_data_with_retry
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


def test_minimal_response_has_one_required_key():
    """Test that a minimal response can contain only one required key."""
    present_keys = set(MOCK_API_RESPONSE_MINIMAL) & set(API_REQUIRED_RESPONSE_JSON_KEYS)
    assert len(present_keys) == 1


def test_optional_keys_present_in_full_response():
    """Test that optional keys are present in full response."""
    for key in API_OPTIONAL_RESPONSE_JSON_KEYS:
        assert key in MOCK_API_RESPONSE_FULL


def test_no_required_key_detected():
    """Test that a response with none of the required keys is invalid."""
    assert not set(MOCK_API_RESPONSE_MISSING_REQUIRED) & set(API_REQUIRED_RESPONSE_JSON_KEYS)


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


async def test_fetch_data_accepts_response_with_one_required_key():
    """A response with one required key is accepted without retrying."""
    response = MagicMock(status=200)
    response.json = AsyncMock(return_value={"power": 2500})
    response_context = AsyncMock()
    response_context.__aenter__.return_value = response
    session = MagicMock()
    session.get.return_value = response_context

    assert await fetch_data_with_retry(session, "http://device/v1/json") == {"power": 2500}

    assert session.get.call_count == 1


async def test_fetch_data_rejects_response_without_required_keys():
    """A response without any recognized key is rejected without retrying."""
    response = MagicMock(status=200)
    response.json = AsyncMock(return_value=MOCK_API_RESPONSE_MISSING_REQUIRED)
    response_context = AsyncMock()
    response_context.__aenter__.return_value = response
    session = MagicMock()
    session.get.return_value = response_context

    with pytest.raises(InvalidData) as err:
        await fetch_data_with_retry(session, "http://device/v1/json")

    assert session.get.call_count == 1
    assert str(MOCK_API_RESPONSE_MISSING_REQUIRED) in str(err.value)
