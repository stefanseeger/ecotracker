"""Tests for Ecotracker diagnostics."""

from __future__ import annotations

from unittest.mock import MagicMock

from custom_components.ecotracker.const import CONF_SCAN_INTERVAL
from custom_components.ecotracker.diagnostics import (
    async_get_config_entry_diagnostics,
    async_get_device_diagnostics,
)


async def test_diagnostics_redact_sensitive_network_data(hass, mock_config_entry, mock_coordinator):
    """Diagnostics redact the IP and SSID while retaining the RSSI."""
    mock_coordinator.data.update({"agePower": 1234, "rssi": -50, "ssid": "FRITZBox-1234"})
    mock_config_entry.runtime_data = mock_coordinator

    diagnostics = await async_get_config_entry_diagnostics(hass, mock_config_entry)

    assert diagnostics == {
        "ip_address": "**REDACTED**",
        "agePower": 1234,
        CONF_SCAN_INTERVAL: 60,
        "rssi": -50,
        "ssid": "**REDACTED**",
    }


async def test_diagnostics_allow_missing_wireless_data(hass, mock_config_entry, mock_coordinator):
    """Diagnostics return None when optional wireless values are absent."""
    mock_config_entry.runtime_data = mock_coordinator

    diagnostics = await async_get_config_entry_diagnostics(hass, mock_config_entry)

    assert diagnostics["ip_address"] == "**REDACTED**"
    assert diagnostics["agePower"] is None
    assert diagnostics[CONF_SCAN_INTERVAL] == 60
    assert diagnostics["rssi"] is None
    assert diagnostics["ssid"] is None


async def test_device_diagnostics_redact_sensitive_network_data(hass, mock_config_entry, mock_coordinator):
    """Device diagnostics redact the IP and SSID while retaining the RSSI."""
    mock_coordinator.data.update({"agePower": 1234, "rssi": -50, "ssid": "FRITZBox-1234"})
    mock_config_entry.runtime_data = mock_coordinator

    diagnostics = await async_get_device_diagnostics(hass, mock_config_entry, MagicMock())

    assert diagnostics["ip_address"] == "**REDACTED**"
    assert diagnostics["agePower"] == 1234
    assert diagnostics["rssi"] == -50
    assert diagnostics["ssid"] == "**REDACTED**"
