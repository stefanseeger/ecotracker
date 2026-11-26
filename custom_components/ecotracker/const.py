"""Constants for the Ecotracker integration."""

DOMAIN = "ecotracker"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 60
CONF_POWER_THRESHOLD = "power_threshold"
DEFAULT_POWER_THRESHOLD = 0
DEFAULT_POWER_HEARTBEAT_INTERVAL = 30.0
CONF_PHASE_POWER_UPDATE_INTERVAL = "phase_power_update_interval"
CONF_POWER_AVG_UPDATE_INTERVAL = "power_avg_update_interval"
CONF_ENERGY_UPDATE_INTERVAL = "energy_update_interval"
CONF_DIAGNOSTIC_UPDATE_INTERVAL = "diagnostic_update_interval"
PHASE_POWER_UPDATE_INTERVAL = 30
POWER_AVG_UPDATE_INTERVAL = 60
ENERGY_UPDATE_INTERVAL = 60
DIAGNOSTIC_UPDATE_INTERVAL = 60
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
