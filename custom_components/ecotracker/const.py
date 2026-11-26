"""Constants for the Ecotracker integration."""

DOMAIN = "ecotracker"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 60
CONF_POWER_THRESHOLD = "power_threshold"
DEFAULT_POWER_THRESHOLD = 0
DEFAULT_POWER_HEARTBEAT_INTERVAL = 30.0
PHASE_POWER_UPDATE_INTERVAL = 30.0
POWER_AVG_UPDATE_INTERVAL = 60.0
ENERGY_UPDATE_INTERVAL = 60.0
DIAGNOSTIC_UPDATE_INTERVAL = 60.0
RSSI_UPDATE_INTERVAL = 300.0
MAX_RETRIES = 3
RETRY_BACKOFF_MULTIPLIER = 2  # Exponential backoff: 1s, 2s, 4s
API_ENDPOINT = "/v1/json"

# At least one of these keys must be present in a valid API response
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
    "rssi",
    "ssid",
]
