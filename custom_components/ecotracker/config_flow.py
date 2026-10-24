"""Config flow for Ecotracker integration."""

from __future__ import annotations

import logging
from typing import Any

import probatio as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import (
    API_ENDPOINT,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .coordinator import InvalidData, fetch_data_with_retry

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=86400)
        ),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ecotracker."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_IP_ADDRESS])
            self._abort_if_unique_id_configured()
            try:
                info = await self.validate_input(user_input)
            except InvalidData:
                errors["base"] = "invalid_data"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Handle reconfiguration of an existing entry."""
        errors: dict[str, str] = {}
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            try:
                await self.validate_input(user_input)
            except InvalidData:
                errors["base"] = "invalid_data"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates=user_input,
                )

        form_data = user_input if user_input is not None else entry.data
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_IP_ADDRESS,
                    default=form_data.get(CONF_IP_ADDRESS, entry.data[CONF_IP_ADDRESS]),
                ): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=form_data.get(
                        CONF_SCAN_INTERVAL,
                        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=86400)),
            }
        )
        return self.async_show_form(step_id="reconfigure", data_schema=data_schema, errors=errors)

    async def validate_input(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate the user input allows us to connect."""
        ip_address = data[CONF_IP_ADDRESS]
        url = f"http://{ip_address}{API_ENDPOINT}"

        session = async_get_clientsession(self.hass)

        try:
            await fetch_data_with_retry(session, url)
        except InvalidData:
            raise
        except UpdateFailed as err:
            raise CannotConnect(f"Validation failed: {err}") from err

        return {"title": f"Ecotracker ({ip_address})"}


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
