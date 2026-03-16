"""Constants for the Ecotracker integration."""

DOMAIN = "ecotracker"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 60
MAX_RETRIES = 3
API_ENDPOINT = "/v1/json"
API_REQUIRED_RESPONSE_JSON_KEYS = [
    "power",
    "powerAvg",
    "energyCounterIn",
    "energyCounterInT1",
    "energyCounterInT2",
    "energyCounterOut",
]
