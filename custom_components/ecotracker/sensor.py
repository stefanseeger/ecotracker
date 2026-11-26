"""Sensor platform for Ecotracker integration."""

from __future__ import annotations

import logging
import time
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_IP_ADDRESS,
    EntityCategory,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import EcotrackerConfigEntry
from .const import (
    CONF_DIAGNOSTIC_UPDATE_INTERVAL,
    CONF_ENERGY_UPDATE_INTERVAL,
    CONF_PHASE_POWER_UPDATE_INTERVAL,
    CONF_POWER_AVG_UPDATE_INTERVAL,
    CONF_POWER_THRESHOLD,
    CONF_SCAN_INTERVAL,
    DEFAULT_POWER_HEARTBEAT_INTERVAL,
    DEFAULT_POWER_THRESHOLD,
    DEFAULT_SCAN_INTERVAL,
    DIAGNOSTIC_UPDATE_INTERVAL,
    DOMAIN,
    ENERGY_UPDATE_INTERVAL,
    PHASE_POWER_UPDATE_INTERVAL,
    POWER_AVG_UPDATE_INTERVAL,
)
from .coordinator import EcotrackerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EcotrackerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ecotracker sensors based on a config entry."""
    coordinator = entry.runtime_data

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
        EcotrackerAgePowerSensor(coordinator, entry),
        EcotrackerScanIntervalSensor(coordinator, entry),
        EcotrackerIPAddressSensor(coordinator, entry),
        EcotrackerRssiSensor(coordinator, entry),
        EcotrackerSsidSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class EcotrackerSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Ecotracker sensors."""

    _min_update_interval: float = 0.0
    _power_deadband: float = 0.0

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_has_entity_name = True
        self._last_write: float | None = None
        self._last_written_value: Any = None
        self._last_available: bool | None = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Write state to Home Assistant, respecting per-sensor throttling and deadband."""
        now = time.monotonic()
        available = self.available
        value = self.native_value if available else None

        # Always publish immediately on first update, availability transitions, or missing values.
        if self._last_write is None or self._last_available != available or not available or value is None:
            self._last_write = now
            self._last_written_value = value
            self._last_available = available
            self.async_write_ha_state()
            return

        elapsed = now - self._last_write
        if self._min_update_interval > 0 and elapsed < self._min_update_interval:
            return

        if (
            self._power_deadband > 0
            and isinstance(value, (int, float))
            and isinstance(self._last_written_value, (int, float))
        ):
            heartbeat = max(self._min_update_interval, DEFAULT_POWER_HEARTBEAT_INTERVAL)
            if abs(value - self._last_written_value) < self._power_deadband and elapsed < heartbeat:
                return

        self._last_write = now
        self._last_written_value = value
        self._last_available = available
        self.async_write_ha_state()

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

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power"
        self._attr_unique_id = f"{entry.entry_id}_power"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._power_deadband = float(entry.data.get(CONF_POWER_THRESHOLD, DEFAULT_POWER_THRESHOLD))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("power")


class EcotrackerPowerPhase1Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Phase 1 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_phase_1"
        self._attr_unique_id = f"{entry.entry_id}_power_phase1"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._min_update_interval = float(entry.data.get(CONF_PHASE_POWER_UPDATE_INTERVAL, PHASE_POWER_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerPhase1")


class EcotrackerPowerPhase2Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Phase 2 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_phase_2"
        self._attr_unique_id = f"{entry.entry_id}_power_phase2"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._min_update_interval = float(entry.data.get(CONF_PHASE_POWER_UPDATE_INTERVAL, PHASE_POWER_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerPhase2")


class EcotrackerPowerPhase3Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Phase 3 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_phase_3"
        self._attr_unique_id = f"{entry.entry_id}_power_phase3"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._min_update_interval = float(entry.data.get(CONF_PHASE_POWER_UPDATE_INTERVAL, PHASE_POWER_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerPhase3")


class EcotrackerPowerAvgSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Power Average Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "power_avg"
        self._attr_unique_id = f"{entry.entry_id}_power_avg"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._min_update_interval = float(entry.data.get(CONF_POWER_AVG_UPDATE_INTERVAL, POWER_AVG_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("powerAvg")


class EcotrackerEnergyInSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter In Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_in"
        self._attr_unique_id = f"{entry.entry_id}_energy_in"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._min_update_interval = float(entry.data.get(CONF_ENERGY_UPDATE_INTERVAL, ENERGY_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterIn")


class EcotrackerEnergyInT1Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter InT1 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_in_t1"
        self._attr_unique_id = f"{entry.entry_id}_energy_in_t1"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._min_update_interval = float(entry.data.get(CONF_ENERGY_UPDATE_INTERVAL, ENERGY_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterInT1")


class EcotrackerEnergyInT2Sensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter InT2 Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_in_t2"
        self._attr_unique_id = f"{entry.entry_id}_energy_in_t2"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._min_update_interval = float(entry.data.get(CONF_ENERGY_UPDATE_INTERVAL, ENERGY_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterInT2")


class EcotrackerEnergyOutSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Energy Counter Out Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "energy_out"
        self._attr_unique_id = f"{entry.entry_id}_energy_out"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._min_update_interval = float(entry.data.get(CONF_ENERGY_UPDATE_INTERVAL, ENERGY_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energyCounterOut")


class EcotrackerAgePowerSensor(EcotrackerSensorBase):
    """Representation of Ecotracker Age Power Sensor."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "age_power"
        self._attr_unique_id = f"{entry.entry_id}_age_power"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_entity_registry_enabled_default = False
        self._attr_native_unit_of_measurement = "ms"
        self._min_update_interval = float(entry.data.get(CONF_DIAGNOSTIC_UPDATE_INTERVAL, DIAGNOSTIC_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("agePower")


class EcotrackerIPAddressSensor(EcotrackerSensorBase):
    """Representation of the configured Ecotracker IP address."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "ip_address"
        self._attr_unique_id = f"{entry.entry_id}_ip_address"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> str:
        """Return the configured IP address."""
        return self._entry.data[CONF_IP_ADDRESS]


class EcotrackerScanIntervalSensor(EcotrackerSensorBase):
    """Representation of the configured polling interval."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "scan_interval"
        self._attr_unique_id = f"{entry.entry_id}_scan_interval"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_native_unit_of_measurement = UnitOfTime.SECONDS

    @property
    def native_value(self) -> int:
        """Return the configured polling interval in seconds."""
        return self._entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)


class EcotrackerRssiSensor(EcotrackerSensorBase):
    """Representation of the Ecotracker Wi-Fi signal strength."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "rssi"
        self._attr_unique_id = f"{entry.entry_id}_rssi"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_entity_registry_enabled_default = False
        self._min_update_interval = float(entry.data.get(CONF_DIAGNOSTIC_UPDATE_INTERVAL, DIAGNOSTIC_UPDATE_INTERVAL))
        self._min_update_interval = float(entry.data.get(CONF_DIAGNOSTIC_UPDATE_INTERVAL, DIAGNOSTIC_UPDATE_INTERVAL))

    @property
    def native_value(self) -> int | None:
        """Return the Wi-Fi signal strength."""
        return self.coordinator.data.get("rssi")


class EcotrackerSsidSensor(EcotrackerSensorBase):
    """Representation of the Ecotracker Wi-Fi network name."""

    def __init__(self, coordinator: EcotrackerCoordinator, entry: EcotrackerConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "ssid"
        self._attr_unique_id = f"{entry.entry_id}_ssid"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> str | None:
        """Return the Wi-Fi network name."""
        return self.coordinator.data.get("ssid")
