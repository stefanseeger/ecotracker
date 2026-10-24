from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_ENDPOINT, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .coordinator import EcotrackerCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]
type EcotrackerConfigEntry = ConfigEntry[EcotrackerCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: EcotrackerConfigEntry) -> bool:
    """Set up Ecotracker from a config entry."""
    ip_address = entry.data[CONF_IP_ADDRESS]
    url = f"http://{ip_address}{API_ENDPOINT}"
    coordinator = EcotrackerCoordinator(
        hass,
        async_get_clientsession(hass),
        url,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: EcotrackerConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
