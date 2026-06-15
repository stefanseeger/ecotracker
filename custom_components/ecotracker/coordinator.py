"""Coordinator for Ecotracker integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    API_REQUIRED_RESPONSE_JSON_KEYS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_RETRIES,
)

_LOGGER = logging.getLogger(__name__)


async def fetch_data_with_retry(
    session: aiohttp.ClientSession,
    url: str,
) -> dict[str, Any]:
    """Fetch data from API endpoint with retry logic."""
    last_error: Exception | None = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            async with async_timeout.timeout(10), session.get(url) as response:
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
                        f"Invalid data received: {data}, missing keys from {API_REQUIRED_RESPONSE_JSON_KEYS}"
                    )

                return data
        except TimeoutError as err:
            last_error = UpdateFailed(f"Timeout error: {err}")
            if attempt < MAX_RETRIES:
                _LOGGER.debug(
                    "Timeout error: %s, Attempt %d failed, retrying...",
                    err,
                    attempt + 1,
                )
                continue
            raise last_error from err
        except aiohttp.ClientError as err:
            last_error = UpdateFailed(f"Error communicating with API: {err}")
            if attempt < MAX_RETRIES:
                _LOGGER.debug(
                    "Client error: %s, Attempt %d failed, retrying...",
                    err,
                    attempt + 1,
                )
                continue
            raise last_error from err
        except UpdateFailed as err:
            last_error = UpdateFailed(f"Unexpected error: {err}")
            if attempt < MAX_RETRIES:
                _LOGGER.debug(
                    "UpdateFailed: %s, Attempt %d failed, retrying...",
                    err,
                    attempt + 1,
                )
                continue
            raise last_error from err
        except Exception as err:
            last_error = UpdateFailed(f"Unexpected error: {err}")
            if attempt < MAX_RETRIES:
                _LOGGER.debug(
                    "Exception: %s, Attempt %d failed, retrying...",
                    err,
                    attempt + 1,
                )
                continue
            raise last_error from err

    # This should never be reached, but satisfy type checker
    raise UpdateFailed("Failed to fetch data after retries")


class EcotrackerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ecotracker data."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        url: str,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
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

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        return await fetch_data_with_retry(self.session, self.url)
