"""Diagnostics support for Ecotracker."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    return {
        "ip_address": entry.data[CONF_IP_ADDRESS],
        "rssi": coordinator.data.get("rssi"),
        "ssid": coordinator.data.get("ssid"),
    }
