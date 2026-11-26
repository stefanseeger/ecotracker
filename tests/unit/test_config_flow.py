"""Tests for Ecotracker config flow."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.data_entry_flow import AbortFlow

from custom_components.ecotracker.config_flow import STEP_USER_DATA_SCHEMA, CannotConnect, ConfigFlow
from custom_components.ecotracker.const import (
    CONF_DIAGNOSTIC_UPDATE_INTERVAL,
    CONF_ENERGY_UPDATE_INTERVAL,
    CONF_PHASE_POWER_UPDATE_INTERVAL,
    CONF_POWER_AVG_UPDATE_INTERVAL,
    CONF_POWER_THRESHOLD,
    CONF_SCAN_INTERVAL,
    DEFAULT_POWER_THRESHOLD,
    DIAGNOSTIC_UPDATE_INTERVAL,
    ENERGY_UPDATE_INTERVAL,
    PHASE_POWER_UPDATE_INTERVAL,
    POWER_AVG_UPDATE_INTERVAL,
)
from custom_components.ecotracker.coordinator import InvalidData
from tests.mock_data import MOCK_ENTRY_DATA


def create_flow() -> ConfigFlow:
    """Return a flow with mocked Home Assistant flow methods."""
    flow = ConfigFlow()
    flow.async_set_unique_id = AsyncMock()
    flow._abort_if_unique_id_configured = MagicMock()
    flow.async_create_entry = MagicMock(return_value={"type": "create_entry"})
    flow.async_show_form = MagicMock(return_value={"type": "form"})
    return flow


async def test_user_flow_creates_entry_and_sets_unique_id():
    """The user flow validates and creates a uniquely identified entry."""
    flow = create_flow()
    flow.validate_input = AsyncMock(return_value={"title": "Ecotracker"})

    result = await flow.async_step_user(MOCK_ENTRY_DATA)

    assert result == {"type": "create_entry"}
    flow.async_set_unique_id.assert_awaited_once_with(MOCK_ENTRY_DATA["ip_address"])
    flow._abort_if_unique_id_configured.assert_called_once_with()
    flow.async_create_entry.assert_called_once_with(title="Ecotracker", data=MOCK_ENTRY_DATA)


async def test_user_flow_aborts_duplicate_before_validating():
    """A duplicate device is aborted before any network validation."""
    flow = create_flow()
    flow._abort_if_unique_id_configured.side_effect = AbortFlow("already_configured")
    flow.validate_input = AsyncMock()

    with pytest.raises(AbortFlow):
        await flow.async_step_user(MOCK_ENTRY_DATA)

    flow.validate_input.assert_not_awaited()


async def test_reconfigure_form_defaults_to_current_entry_data():
    """The reconfigure form is prefilled with saved settings and default intervals."""
    flow = create_flow()
    entry = MagicMock(data={"ip_address": "192.168.1.42", CONF_SCAN_INTERVAL: 30})
    flow._get_reconfigure_entry = MagicMock(return_value=entry)

    result = await flow.async_step_reconfigure()

    assert result == {"type": "form"}
    data_schema = flow.async_show_form.call_args.kwargs["data_schema"]
    assert data_schema({}) == {
        "ip_address": "192.168.1.42",
        CONF_SCAN_INTERVAL: 30,
        CONF_POWER_THRESHOLD: DEFAULT_POWER_THRESHOLD,
        CONF_PHASE_POWER_UPDATE_INTERVAL: PHASE_POWER_UPDATE_INTERVAL,
        CONF_POWER_AVG_UPDATE_INTERVAL: POWER_AVG_UPDATE_INTERVAL,
        CONF_ENERGY_UPDATE_INTERVAL: ENERGY_UPDATE_INTERVAL,
        CONF_DIAGNOSTIC_UPDATE_INTERVAL: DIAGNOSTIC_UPDATE_INTERVAL,
    }


async def test_reconfigure_form_preserves_submitted_data_after_error():
    """The reconfigure form keeps submitted values after a validation error."""
    flow = create_flow()
    entry = MagicMock(data={"ip_address": "192.168.1.42", CONF_SCAN_INTERVAL: 30})
    flow._get_reconfigure_entry = MagicMock(return_value=entry)
    flow.validate_input = AsyncMock(side_effect=CannotConnect("offline"))
    user_input = {
        "ip_address": "192.168.1.99",
        CONF_SCAN_INTERVAL: 45,
        CONF_POWER_THRESHOLD: 10,
        CONF_PHASE_POWER_UPDATE_INTERVAL: 15,
        CONF_POWER_AVG_UPDATE_INTERVAL: 30,
        CONF_ENERGY_UPDATE_INTERVAL: 120,
        CONF_DIAGNOSTIC_UPDATE_INTERVAL: 90,
    }

    result = await flow.async_step_reconfigure(user_input)

    assert result == {"type": "form"}
    data_schema = flow.async_show_form.call_args.kwargs["data_schema"]
    assert data_schema({}) == user_input


@pytest.mark.parametrize(
    ("error", "error_key"),
    [
        (CannotConnect("offline"), "cannot_connect"),
        (InvalidData("invalid"), "invalid_data"),
        (Exception("unexpected"), "unknown"),
    ],
)
async def test_user_flow_shows_errors_and_can_recover(error, error_key):
    """Flow errors are shown and the user can submit valid input afterward."""
    flow = create_flow()
    flow.validate_input = AsyncMock(side_effect=error)

    result = await flow.async_step_user(MOCK_ENTRY_DATA)

    assert result == {"type": "form"}
    flow.async_show_form.assert_called_once_with(
        step_id="user",
        data_schema=flow.async_show_form.call_args.kwargs["data_schema"],
        errors={"base": error_key},
    )

    flow.validate_input.side_effect = None
    flow.validate_input.return_value = {"title": "Ecotracker"}
    result = await flow.async_step_user(MOCK_ENTRY_DATA)

    assert result == {"type": "create_entry"}


def test_translation_files_cover_user_and_reconfigure_steps():
    """All translation files define every config flow field for both user and reconfigure steps."""
    integration_dir = Path(__file__).resolve().parents[2] / "custom_components" / "ecotracker"
    translation_files = [integration_dir / "strings.json", *sorted((integration_dir / "translations").glob("*.json"))]
    expected_fields = {key.schema for key in STEP_USER_DATA_SCHEMA.schema}
    expected_descriptions = expected_fields - {"ip_address"}

    for translation_file in translation_files:
        payload = json.loads(translation_file.read_text(encoding="utf-8"))
        steps = payload["config"]["step"]
        for step_id in ("user", "reconfigure"):
            assert step_id in steps, f"{translation_file.name} missing config.step.{step_id}"
            step = steps[step_id]
            assert step.get("title"), f"{translation_file.name} missing {step_id}.title"
            assert step.get("description"), f"{translation_file.name} missing {step_id}.description"
            assert expected_fields <= set(step.get("data", {})), f"{translation_file.name} missing {step_id}.data keys"
            assert expected_descriptions <= set(step.get("data_description", {})), (
                f"{translation_file.name} missing {step_id}.data_description keys"
            )
