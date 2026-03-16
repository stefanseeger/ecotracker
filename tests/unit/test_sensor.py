"""Tests for Ecotracker sensors."""

from __future__ import annotations

from unittest.mock import MagicMock

from homeassistant.const import UnitOfEnergy, UnitOfPower

from custom_components.ecotracker.const import DOMAIN
from custom_components.ecotracker.sensor import (
    EcotrackerEnergyInSensor,
    EcotrackerEnergyInT1Sensor,
    EcotrackerEnergyInT2Sensor,
    EcotrackerEnergyOutSensor,
    EcotrackerPowerAvgSensor,
    EcotrackerPowerPhase1Sensor,
    EcotrackerPowerPhase2Sensor,
    EcotrackerPowerPhase3Sensor,
    EcotrackerPowerSensor,
)
from tests.mock_data import TEST_ENTRY_ID


def create_mock_entry():
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = TEST_ENTRY_ID
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
