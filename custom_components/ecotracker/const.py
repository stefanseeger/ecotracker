"""Constants for the Ecotracker integration."""

DOMAIN = "ecotracker"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 60
API_ENDPOINT = "/v1/json"
API_RESPONSE_JSON_KEYS = [
    "power",
    "powerPhase1",
    "powerPhase2",
    "powerPhase3",
    "powerAvg",
    "energyCounterIn",
    "energyCounterOut",
]