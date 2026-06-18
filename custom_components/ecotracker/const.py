"""Constants for the Ecotracker integration."""

DOMAIN = "ecotracker"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 60
MAX_RETRIES = 3
RETRY_BACKOFF_MULTIPLIER = 2  # Exponential backoff: 1s, 2s, 4s
API_ENDPOINT = "/v1/json"

# Required keys must be present in API response for valid data
API_REQUIRED_RESPONSE_JSON_KEYS = [
    "power",
    "powerAvg",
    "energyCounterIn",
]

# Optional keys that may be present depending on device capabilities
API_OPTIONAL_RESPONSE_JSON_KEYS = [
    "powerPhase1",
    "powerPhase2",
    "powerPhase3",
    "energyCounterInT1",
    "energyCounterInT2",
    "energyCounterOut",
    "agePower",
]
