"""Tests for Ecotracker config flow."""

from __future__ import annotations

from custom_components.ecotracker.config_flow import ConfigFlow


def test_config_flow_instantiation():
    """Test ConfigFlow can be instantiated."""
    flow = ConfigFlow()
    assert flow is not None
    assert flow.VERSION == 1
    assert flow.MINOR_VERSION == 1


def test_config_flow_version():
    """Test ConfigFlow has correct version."""
    flow = ConfigFlow()
    assert flow.VERSION == 1


def test_config_flow_constants():
    """Test ConfigFlow constants."""
    flow = ConfigFlow()
    assert hasattr(flow, "VERSION")
    assert hasattr(flow, "MINOR_VERSION")
