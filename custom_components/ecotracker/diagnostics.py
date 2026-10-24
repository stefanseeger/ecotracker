"""Diagnostics support for Ecotracker."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from . import EcotrackerConfigEntry
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

TO_REDACT = {CONF_IP_ADDRESS, "ssid"}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: EcotrackerConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return async_redact_data(
        {
            CONF_IP_ADDRESS: entry.data[CONF_IP_ADDRESS],
            "agePower": coordinator.data.get("agePower"),
            CONF_SCAN_INTERVAL: entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            "rssi": coordinator.data.get("rssi"),
            "ssid": coordinator.data.get("ssid"),
        },
        TO_REDACT,
    )


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: EcotrackerConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device."""
    return await async_get_config_entry_diagnostics(hass, entry)
