"""Tests for Ecotracker sensors."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from homeassistant.const import EntityCategory, UnitOfEnergy, UnitOfPower, UnitOfTime

from custom_components.ecotracker.const import (
    CONF_ENERGY_UPDATE_INTERVAL,
    CONF_PHASE_POWER_UPDATE_INTERVAL,
    CONF_POWER_THRESHOLD,
    CONF_SCAN_INTERVAL,
    DEFAULT_POWER_HEARTBEAT_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DIAGNOSTIC_UPDATE_INTERVAL,
    DOMAIN,
    ENERGY_UPDATE_INTERVAL,
    PHASE_POWER_UPDATE_INTERVAL,
)
from custom_components.ecotracker.sensor import (
    EcotrackerAgePowerSensor,
    EcotrackerEnergyInSensor,
    EcotrackerEnergyInT1Sensor,
    EcotrackerEnergyInT2Sensor,
    EcotrackerEnergyOutSensor,
    EcotrackerIPAddressSensor,
    EcotrackerPowerAvgSensor,
    EcotrackerPowerPhase1Sensor,
    EcotrackerPowerPhase2Sensor,
    EcotrackerPowerPhase3Sensor,
    EcotrackerPowerSensor,
    EcotrackerRssiSensor,
    EcotrackerScanIntervalSensor,
    EcotrackerSsidSensor,
)
from tests.mock_data import TEST_ENTRY_ID


def create_mock_entry():
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = TEST_ENTRY_ID
    entry.data = {"ip_address": "192.168.1.100"}
    return entry


def create_mock_coordinator(data: dict):
    """Create a mock coordinator with given data."""
    coordinator = MagicMock()
    coordinator.data = data
    return coordinator


def test_power_sensor_properties():
    """Test EcotrackerPowerSensor properties."""
    coordinator = create_mock_coordinator({"power": 2500})
    entry = create_mock_entry()

    sensor = EcotrackerPowerSensor(coordinator, entry)

    assert sensor.native_value == 2500
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_power"
    assert sensor.translation_key == "power"


def test_power_avg_sensor_properties():
    """Test EcotrackerPowerAvgSensor properties."""
    coordinator = create_mock_coordinator({"powerAvg": 2400})
    entry = create_mock_entry()

    sensor = EcotrackerPowerAvgSensor(coordinator, entry)

    assert sensor.native_value == 2400
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_power_avg"
    assert sensor.translation_key == "power_avg"


def test_power_phase1_sensor_properties():
    """Test EcotrackerPowerPhase1Sensor properties."""
    coordinator = create_mock_coordinator({"powerPhase1": 850})
    entry = create_mock_entry()

    sensor = EcotrackerPowerPhase1Sensor(coordinator, entry)

    assert sensor.native_value == 850
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_power_phase1"
    assert sensor.translation_key == "power_phase_1"


def test_power_phase2_sensor_properties():
    """Test EcotrackerPowerPhase2Sensor properties."""
    coordinator = create_mock_coordinator({"powerPhase2": 800})
    entry = create_mock_entry()

    sensor = EcotrackerPowerPhase2Sensor(coordinator, entry)

    assert sensor.native_value == 800
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_power_phase2"


def test_power_phase3_sensor_properties():
    """Test EcotrackerPowerPhase3Sensor properties."""
    coordinator = create_mock_coordinator({"powerPhase3": 850})
    entry = create_mock_entry()

    sensor = EcotrackerPowerPhase3Sensor(coordinator, entry)

    assert sensor.native_value == 850
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_power_phase3"


def test_energy_in_sensor_properties():
    """Test EcotrackerEnergyInSensor properties."""
    coordinator = create_mock_coordinator({"energyCounterIn": 50000})
    entry = create_mock_entry()

    sensor = EcotrackerEnergyInSensor(coordinator, entry)

    assert sensor.native_value == 50000
    assert sensor.native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_energy_in"
    assert sensor.translation_key == "energy_in"


def test_energy_in_t1_sensor_properties():
    """Test EcotrackerEnergyInT1Sensor properties."""
    coordinator = create_mock_coordinator({"energyCounterInT1": 25000})
    entry = create_mock_entry()

    sensor = EcotrackerEnergyInT1Sensor(coordinator, entry)

    assert sensor.native_value == 25000
    assert sensor.native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_energy_in_t1"


def test_energy_in_t2_sensor_properties():
    """Test EcotrackerEnergyInT2Sensor properties."""
    coordinator = create_mock_coordinator({"energyCounterInT2": 25000})
    entry = create_mock_entry()

    sensor = EcotrackerEnergyInT2Sensor(coordinator, entry)

    assert sensor.native_value == 25000
    assert sensor.native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_energy_in_t2"


def test_energy_out_sensor_properties():
    """Test EcotrackerEnergyOutSensor properties."""
    coordinator = create_mock_coordinator({"energyCounterOut": 5000})
    entry = create_mock_entry()

    sensor = EcotrackerEnergyOutSensor(coordinator, entry)

    assert sensor.native_value == 5000
    assert sensor.native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_energy_out"


def test_sensor_device_info():
    """Test that sensors have correct device info."""
    coordinator = create_mock_coordinator({"power": 2500})
    entry = create_mock_entry()

    sensor = EcotrackerPowerSensor(coordinator, entry)
    device_info = sensor.device_info

    assert device_info is not None
    assert (DOMAIN, TEST_ENTRY_ID) in device_info["identifiers"]  # pyright: ignore[reportTypedDictNotRequiredAccess]
    assert device_info["name"] == "Ecotracker"  # pyright: ignore[reportTypedDictNotRequiredAccess]


def test_sensor_native_value_missing_key():
    """Test sensor returns None when coordinator key is missing."""
    coordinator = create_mock_coordinator({})
    entry = create_mock_entry()

    sensor = EcotrackerPowerSensor(coordinator, entry)

    assert sensor.native_value is None


def test_sensor_has_entity_name():
    """Test sensors have entity name enabled."""
    coordinator = create_mock_coordinator({"power": 2500})
    entry = create_mock_entry()

    sensor = EcotrackerPowerSensor(coordinator, entry)

    assert sensor.has_entity_name is True


def test_age_power_sensor_properties():
    """Test EcotrackerAgePowerSensor properties."""
    coordinator = create_mock_coordinator({"agePower": 5000})
    entry = create_mock_entry()

    sensor = EcotrackerAgePowerSensor(coordinator, entry)

    assert sensor.native_value == 5000
    assert sensor.native_unit_of_measurement == "ms"
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_age_power"
    assert sensor.translation_key == "age_power"
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.entity_registry_enabled_default is False
    assert sensor.state_class is None


def test_age_power_sensor_no_value():
    """Test EcotrackerAgePowerSensor returns None when value is missing."""
    coordinator = create_mock_coordinator({})
    entry = create_mock_entry()

    sensor = EcotrackerAgePowerSensor(coordinator, entry)

    assert sensor.native_value is None


def test_ip_address_diagnostic_sensor():
    """Test configured IP diagnostic sensor properties."""
    sensor = EcotrackerIPAddressSensor(create_mock_coordinator({}), create_mock_entry())

    assert sensor.native_value == "192.168.1.100"
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_ip_address"


def test_scan_interval_diagnostic_sensor_properties():
    """Test configured polling interval diagnostic sensor properties."""
    entry = create_mock_entry()
    entry.data[CONF_SCAN_INTERVAL] = 30
    sensor = EcotrackerScanIntervalSensor(create_mock_coordinator({}), entry)

    assert sensor.native_value == 30
    assert sensor.native_unit_of_measurement == UnitOfTime.SECONDS
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_scan_interval"
    assert sensor.translation_key == "scan_interval"


def test_scan_interval_diagnostic_sensor_uses_default_for_existing_entry():
    """Test older entries without an interval use the default."""
    sensor = EcotrackerScanIntervalSensor(create_mock_coordinator({}), create_mock_entry())

    assert sensor.native_value == DEFAULT_SCAN_INTERVAL


def test_rssi_diagnostic_sensor():
    """Test RSSI diagnostic sensor properties and missing data."""
    entry = create_mock_entry()
    sensor = EcotrackerRssiSensor(create_mock_coordinator({"rssi": -50}), entry)
    missing_sensor = EcotrackerRssiSensor(create_mock_coordinator({}), entry)

    assert sensor.native_value == -50
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.entity_registry_enabled_default is False
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_rssi"
    assert missing_sensor.native_value is None


def test_ssid_diagnostic_sensor():
    """Test SSID diagnostic sensor properties and missing data."""
    entry = create_mock_entry()
    sensor = EcotrackerSsidSensor(create_mock_coordinator({"ssid": "FRITZBox-1234"}), entry)
    missing_sensor = EcotrackerSsidSensor(create_mock_coordinator({}), entry)

    assert sensor.native_value == "FRITZBox-1234"
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.unique_id == f"{TEST_ENTRY_ID}_ssid"
    assert missing_sensor.native_value is None


def test_energy_sensor_throttles_frequent_updates():
    """Energy sensors write at most once per ENERGY_UPDATE_INTERVAL."""
    coordinator = create_mock_coordinator({"energyCounterIn": 50000})
    coordinator.last_update_success = True
    sensor = EcotrackerEnergyInSensor(coordinator, create_mock_entry())
    sensor.async_write_ha_state = MagicMock()

    with patch("custom_components.ecotracker.sensor.time.monotonic", side_effect=[100.0, 101.0, 159.0, 160.0]):
        sensor._handle_coordinator_update()
        coordinator.data = {"energyCounterIn": 50001}
        sensor._handle_coordinator_update()
        coordinator.data = {"energyCounterIn": 50002}
        sensor._handle_coordinator_update()
        coordinator.data = {"energyCounterIn": 50003}
        sensor._handle_coordinator_update()

    assert ENERGY_UPDATE_INTERVAL == 60.0
    assert sensor.async_write_ha_state.call_count == 2


def test_phase_and_rssi_sensors_throttle_updates():
    """Phase power and RSSI sensors throttle state writes to their configured intervals."""
    coordinator = create_mock_coordinator({"powerPhase1": 800, "rssi": -50})
    coordinator.last_update_success = True
    entry = create_mock_entry()

    phase_sensor = EcotrackerPowerPhase1Sensor(coordinator, entry)
    phase_sensor.async_write_ha_state = MagicMock()
    with patch(
        "custom_components.ecotracker.sensor.time.monotonic",
        side_effect=[10.0, 10.0 + PHASE_POWER_UPDATE_INTERVAL - 1, 10.0 + PHASE_POWER_UPDATE_INTERVAL],
    ):
        phase_sensor._handle_coordinator_update()
        phase_sensor._handle_coordinator_update()
        phase_sensor._handle_coordinator_update()
    assert phase_sensor.async_write_ha_state.call_count == 2

    rssi_sensor = EcotrackerRssiSensor(coordinator, entry)
    rssi_sensor.async_write_ha_state = MagicMock()
    with patch(
        "custom_components.ecotracker.sensor.time.monotonic",
        side_effect=[10.0, 10.0 + DIAGNOSTIC_UPDATE_INTERVAL - 1, 10.0 + DIAGNOSTIC_UPDATE_INTERVAL],
    ):
        rssi_sensor._handle_coordinator_update()
        rssi_sensor._handle_coordinator_update()
        rssi_sensor._handle_coordinator_update()
    assert rssi_sensor.async_write_ha_state.call_count == 2


def test_power_sensor_deadband_suppresses_jitter_and_keeps_fast_steps():
    """Power deadband filters small jitter, reports large steps immediately, and refreshes on heartbeat."""
    coordinator = create_mock_coordinator({"power": 250})
    coordinator.last_update_success = True
    entry = create_mock_entry()
    entry.data[CONF_POWER_THRESHOLD] = 5
    sensor = EcotrackerPowerSensor(coordinator, entry)
    sensor.async_write_ha_state = MagicMock()

    with patch(
        "custom_components.ecotracker.sensor.time.monotonic",
        side_effect=[100.0, 101.0, 102.0, 102.0 + DEFAULT_POWER_HEARTBEAT_INTERVAL],
    ):
        # First update always writes
        sensor._handle_coordinator_update()
        # Small +3 W jitter (< 5 W) is suppressed
        coordinator.data = {"power": 253}
        sensor._handle_coordinator_update()
        # Large +1000 W step (>= 5 W) writes immediately
        coordinator.data = {"power": 1250}
        sensor._handle_coordinator_update()
        # Small +2 W jitter after heartbeat (>= 30 s) writes
        coordinator.data = {"power": 1252}
        sensor._handle_coordinator_update()

    assert sensor.async_write_ha_state.call_count == 3


def test_power_sensor_default_threshold_writes_every_update():
    """With default power_threshold=0, every power update writes immediately."""
    coordinator = create_mock_coordinator({"power": 250})
    coordinator.last_update_success = True
    sensor = EcotrackerPowerSensor(coordinator, create_mock_entry())
    sensor.async_write_ha_state = MagicMock()

    with patch("custom_components.ecotracker.sensor.time.monotonic", side_effect=[100.0, 101.0, 102.0]):
        sensor._handle_coordinator_update()
        coordinator.data = {"power": 251}
        sensor._handle_coordinator_update()
        coordinator.data = {"power": 252}
        sensor._handle_coordinator_update()

    assert sensor.async_write_ha_state.call_count == 3


def test_throttled_sensor_writes_immediately_on_availability_change():
    """Availability drops and recoveries bypass throttling."""
    coordinator = create_mock_coordinator({"energyCounterIn": 50000})
    coordinator.last_update_success = True
    sensor = EcotrackerEnergyInSensor(coordinator, create_mock_entry())
    sensor.async_write_ha_state = MagicMock()

    with patch("custom_components.ecotracker.sensor.time.monotonic", side_effect=[100.0, 101.0, 102.0]):
        sensor._handle_coordinator_update()
        coordinator.last_update_success = False
        sensor._handle_coordinator_update()
        coordinator.last_update_success = True
        sensor._handle_coordinator_update()

    assert sensor.async_write_ha_state.call_count == 3


def test_throttled_sensor_recovers_immediately_after_missing_value():
    """Recovery from a missing value publishes immediately while subsequent valid updates stay throttled."""
    coordinator = create_mock_coordinator({"energyCounterIn": 50000})
    coordinator.last_update_success = True
    sensor = EcotrackerEnergyInSensor(coordinator, create_mock_entry())
    sensor.async_write_ha_state = MagicMock()

    with patch("custom_components.ecotracker.sensor.time.monotonic", side_effect=[100.0, 101.0, 102.0, 103.0]):
        # Initial valid value writes
        sensor._handle_coordinator_update()
        # Missing value writes immediately (availability stays True)
        coordinator.data = {}
        sensor._handle_coordinator_update()
        # Recovery to valid value writes immediately despite elapsed < ENERGY_UPDATE_INTERVAL
        coordinator.data = {"energyCounterIn": 50005}
        sensor._handle_coordinator_update()
        # Next valid value within throttle window is suppressed
        coordinator.data = {"energyCounterIn": 50010}
        sensor._handle_coordinator_update()

    assert sensor.async_write_ha_state.call_count == 3


def test_custom_configured_update_intervals_override_defaults():
    """Configured per-sensor intervals from entry.data override defaults (including 0 to disable throttling)."""
    coordinator = create_mock_coordinator({"energyCounterIn": 50000, "powerPhase1": 800})
    coordinator.last_update_success = True
    entry = create_mock_entry()
    entry.data[CONF_ENERGY_UPDATE_INTERVAL] = 10
    entry.data[CONF_PHASE_POWER_UPDATE_INTERVAL] = 0

    energy_sensor = EcotrackerEnergyInSensor(coordinator, entry)
    energy_sensor.async_write_ha_state = MagicMock()
    with patch("custom_components.ecotracker.sensor.time.monotonic", side_effect=[100.0, 105.0, 110.0]):
        energy_sensor._handle_coordinator_update()
        energy_sensor._handle_coordinator_update()
        energy_sensor._handle_coordinator_update()
    assert energy_sensor.async_write_ha_state.call_count == 2

    phase_sensor = EcotrackerPowerPhase1Sensor(coordinator, entry)
    phase_sensor.async_write_ha_state = MagicMock()
    with patch("custom_components.ecotracker.sensor.time.monotonic", side_effect=[100.0, 101.0, 102.0]):
        phase_sensor._handle_coordinator_update()
        phase_sensor._handle_coordinator_update()
        phase_sensor._handle_coordinator_update()
    assert phase_sensor.async_write_ha_state.call_count == 3
