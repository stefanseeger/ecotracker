"""Tests for Ecotracker diagnostics."""

from __future__ import annotations

from custom_components.ecotracker.const import DOMAIN
from custom_components.ecotracker.diagnostics import (
    async_get_config_entry_diagnostics,
)


async def test_diagnostics_include_ip_and_wireless_data(hass, mock_config_entry, mock_coordinator):
    """Diagnostics include the configured IP and wireless response values."""
    mock_coordinator.data.update({"rssi": -50, "ssid": "FRITZBox-1234"})
    hass.data[DOMAIN] = {mock_config_entry.entry_id: mock_coordinator}

    diagnostics = await async_get_config_entry_diagnostics(hass, mock_config_entry)

    assert diagnostics == {
        "ip_address": "192.168.1.100",
        "rssi": -50,
        "ssid": "FRITZBox-1234",
    }


async def test_diagnostics_allow_missing_wireless_data(hass, mock_config_entry, mock_coordinator):
    """Diagnostics return None when optional wireless values are absent."""
    hass.data[DOMAIN] = {mock_config_entry.entry_id: mock_coordinator}

    diagnostics = await async_get_config_entry_diagnostics(hass, mock_config_entry)

    assert diagnostics["rssi"] is None
    assert diagnostics["ssid"] is None
