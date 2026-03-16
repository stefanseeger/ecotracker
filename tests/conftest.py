"""Pytest configuration and fixtures for Ecotracker integration tests."""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from tests.mock_data import MOCK_ENTRY_DATA, TEST_ENTRY_ID


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def hass() -> HomeAssistant:
    """Create and yield a Home Assistant instance."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        hass_instance = HomeAssistant(tmpdir)
        await hass_instance.async_block_till_done()
        yield hass_instance
        await hass_instance.async_block_till_done()
        await hass_instance.async_stop()


@pytest.fixture
def mock_coordinator_data() -> dict[str, Any]:
    """Return mock coordinator data."""
    return {
        "power": 2500,
        "powerAvg": 2400,
        "powerPhase1": 850,
        "powerPhase2": 800,
        "powerPhase3": 850,
        "energyCounterIn": 50000,
        "energyCounterInT1": 25000,
        "energyCounterInT2": 25000,
        "energyCounterOut": 5000,
    }


@pytest.fixture
def mock_coordinator(mock_coordinator_data):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_coordinator_data
    coordinator.last_update_success = True
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = TEST_ENTRY_ID
    entry.data = MOCK_ENTRY_DATA
    entry.options = {}
    entry.title = "Ecotracker (192.168.1.100)"
    return entry


@pytest.fixture
def mock_api_response_success(mock_coordinator_data):
    """Create a mock successful API response."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_coordinator_data)
    return mock_response


@pytest.fixture
def mock_api_response_error():
    """Create a mock failed API response."""
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.json = AsyncMock()
    return mock_response
