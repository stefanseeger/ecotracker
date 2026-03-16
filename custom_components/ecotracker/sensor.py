"""Sensor platform for Ecotracker integration."""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
import async_timeout
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    API_ENDPOINT,
    API_REQUIRED_RESPONSE_JSON_KEYS,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_RETRIES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ecotracker sensors based on a config entry."""
    ip_address = entry.data[CONF_IP_ADDRESS]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    url = f"http://{ip_address}{API_ENDPOINT}"

    session = async_get_clientsession(hass)
    coordinator = EcotrackerCoordinator(hass, session, url, scan_interval)

    await coordinator.async_config_entry_first_refresh()

    entities = [
        EcotrackerPowerSensor(coordinator, entry),
        EcotrackerPowerPhase1Sensor(coordinator, entry),
        EcotrackerPowerPhase2Sensor(coordinator, entry),
        EcotrackerPowerPhase3Sensor(coordinator, entry),
        EcotrackerPowerAvgSensor(coordinator, entry),
        EcotrackerEnergyInSensor(coordinator, entry),
        EcotrackerEnergyInT1Sensor(coordinator, entry),
        EcotrackerEnergyInT2Sensor(coordinator, entry),
        EcotrackerEnergyOutSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class EcotrackerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ecotracker data."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        url: str,
        scan_interval: int,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.session = session
        self.url = url

    async def _async_update_data(self):
        """Fetch data from API endpoint."""

        for attempt in range(MAX_RETRIES + 1):
            try:
                async with async_timeout.timeout(10), self.session.get(self.url) as response:
                    if response.status != 200:
                        if attempt < MAX_RETRIES:
                            _LOGGER.debug(
                                "Error fetching data: %s, Attempt %d failed, retrying...",
                                response.status,
                                attempt + 1,
                            )
                            continue
                        raise UpdateFailed(f"Error fetching data: HTTP {response.status}")
                    data = await response.json()

                    if not any(key in data for key in API_REQUIRED_RESPONSE_JSON_KEYS):
                        if attempt < MAX_RETRIES:
                            _LOGGER.debug(
                                "Invalid data received: %s, missing keys from %s, Attempt %d failed, retrying...",
                                data,
                                API_REQUIRED_RESPONSE_JSON_KEYS,
                                attempt + 1,
                            )
                            continue
                        raise UpdateFailed(
                            "Invalid data received: %s, missing keys from %s",
                            data,
                            API_REQUIRED_RESPONSE_JSON_KEYS,
                        )

                    return data
            except asyncio.TimeoutError as err:
                if attempt < MAX_RETRIES:
                    _LOGGER.debug(
                        "Timeout error: %s, Attempt %d failed, retrying...",
                        err,
                        attempt + 1,
                    )
                    continue
                raise UpdateFailed(f"Timeout error: {err}") from err
            except aiohttp.ClientError as err:
                if attempt < MAX_RETRIES:
                    _LOGGER.debug(
                        "Client error: %s, Attempt %d failed, retrying...",
                        err,
                        attempt + 1,
                    )
                    continue
                raise UpdateFailed(f"Error communicating with API: {err}") from err
            except UpdateFailed as err:
                if attempt < MAX_RETRIES:
                    _LOGGER.debug(
                        "UpdateFailed: %s, Attempt %d failed, retrying...",
                        err,
                        attempt + 1,
                    )
                    continue
                raise UpdateFailed(f"Unexpected error: {err}") from err
            except Exception as err:
                if attempt < MAX_RETRIES:
                    _LOGGER.debug(
                        "Exception: %s, Attempt %d failed, retrying...",
                        err,
                        attempt + 1,
                    )
                    continue
                raise UpdateFailed(f"Unexpected error: {err}") from err


class EcotrackerSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Ecotracker sensors."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Ecotracker",
            manufacturer="Ecotracker",
            model="Energy Monitor",
        )


class EcotrackerPowerSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power"
        self._attr_unique_id = f"{entry.entry_id}_power"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("power")


class EcotrackerPowerPhase1Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Phase 1 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_phase_1"
        self._attr_unique_id = f"{entry.entry_id}_power_phase1"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerPhase1")


class EcotrackerPowerPhase2Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Phase 2 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_phase_2"
        self._attr_unique_id = f"{entry.entry_id}_power_phase2"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerPhase2")


class EcotrackerPowerPhase3Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Phase 3 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_phase_3"
        self._attr_unique_id = f"{entry.entry_id}_power_phase3"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerPhase3")


class EcotrackerPowerAvgSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Average Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_avg"
        self._attr_unique_id = f"{entry.entry_id}_power_avg"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerAvg")


class EcotrackerEnergyInSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter In Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_in"
        self._attr_unique_id = f"{entry.entry_id}_energy_in"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterIn")


class EcotrackerEnergyInT1Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter InT1 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_in_t1"
        self._attr_unique_id = f"{entry.entry_id}_energy_in_t1"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterInT1")


class EcotrackerEnergyInT2Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter InT2 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_in_t2"
        self._attr_unique_id = f"{entry.entry_id}_energy_in_t2"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterInT2")


class EcotrackerEnergyOutSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter Out Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_out"
        self._attr_unique_id = f"{entry.entry_id}_energy_out"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterOut")
