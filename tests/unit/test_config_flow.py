"""Tests for Ecotracker config flow."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.data_entry_flow import AbortFlow

from custom_components.ecotracker.config_flow import CannotConnect, ConfigFlow
from custom_components.ecotracker.const import CONF_SCAN_INTERVAL
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
    """The reconfigure form is prefilled with the saved IP and interval."""
    flow = create_flow()
    entry = MagicMock(data={"ip_address": "192.168.1.42", CONF_SCAN_INTERVAL: 30})
    flow._get_reconfigure_entry = MagicMock(return_value=entry)

    result = await flow.async_step_reconfigure()

    assert result == {"type": "form"}
    data_schema = flow.async_show_form.call_args.kwargs["data_schema"]
    assert data_schema({}) == {"ip_address": "192.168.1.42", CONF_SCAN_INTERVAL: 30}


async def test_reconfigure_form_preserves_submitted_data_after_error():
    """The reconfigure form keeps submitted values after a validation error."""
    flow = create_flow()
    entry = MagicMock(data={"ip_address": "192.168.1.42", CONF_SCAN_INTERVAL: 30})
    flow._get_reconfigure_entry = MagicMock(return_value=entry)
    flow.validate_input = AsyncMock(side_effect=CannotConnect("offline"))
    user_input = {"ip_address": "192.168.1.99", CONF_SCAN_INTERVAL: 45}

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
