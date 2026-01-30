"""Constants for the Ecotracker integration."""

DOMAIN = "ecotracker"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 60
API_ENDPOINT = "/v1/json"
API_REQUIRED_RESPONSE_JSON_KEYS = [
    "power",
    "powerAvg",
    "energyCounterIn",
    "energyCounterOut",
]
