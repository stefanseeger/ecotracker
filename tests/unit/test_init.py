"""Tests for Ecotracker config entry setup and unload."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.ecotracker import async_setup_entry, async_unload_entry
from custom_components.ecotracker.const import API_ENDPOINT
from tests.mock_data import MOCK_ENTRY_DATA


async def test_setup_entry_initializes_and_stores_coordinator():
    """Setup performs the initial refresh before forwarding the platform."""
    hass = MagicMock()
    hass.config_entries.async_forward_entry_setups = AsyncMock()
    entry = MagicMock(data=MOCK_ENTRY_DATA)
    coordinator = MagicMock()
    coordinator.async_config_entry_first_refresh = AsyncMock()

    with (
        patch(
            "custom_components.ecotracker.async_get_clientsession",
            return_value=MagicMock(),
        ),
        patch(
            "custom_components.ecotracker.EcotrackerCoordinator",
            return_value=coordinator,
        ) as coordinator_factory,
    ):
        assert await async_setup_entry(hass, entry)

    assert entry.runtime_data is coordinator
    coordinator_factory.assert_called_once_with(
        hass,
        coordinator_factory.call_args.args[1],
        f"http://{MOCK_ENTRY_DATA['ip_address']}{API_ENDPOINT}",
        MOCK_ENTRY_DATA["scan_interval"],
    )
    coordinator.async_config_entry_first_refresh.assert_awaited_once_with()
    hass.config_entries.async_forward_entry_setups.assert_awaited_once()


async def test_unload_entry_unloads_platforms():
    """Unload delegates cleanup to the config entry manager."""
    hass = MagicMock()
    hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)
    entry = MagicMock()

    assert await async_unload_entry(hass, entry)

    hass.config_entries.async_unload_platforms.assert_awaited_once()
