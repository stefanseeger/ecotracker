"""Mock data for Ecotracker integration tests."""

# Valid API response with all required fields
MOCK_API_RESPONSE_FULL = {
    "power": 2500,
    "powerAvg": 2400,
    "powerPhase1": 850,
    "powerPhase2": 800,
    "powerPhase3": 850,
    "energyCounterIn": 50000,
    "energyCounterInT1": 25000,
    "energyCounterInT2": 25000,
    "energyCounterOut": 5000,
}

# Minimal valid API response with only required fields
MOCK_API_RESPONSE_MINIMAL = {
    "power": 1000,
    "powerAvg": 950,
    "energyCounterIn": 30000,
}

# Invalid response: missing required field
MOCK_API_RESPONSE_MISSING_REQUIRED = {
    "power": 2500,
    "powerAvg": 2400,
    # Missing energyCounterIn
}

# Invalid response: invalid data type (string instead of number)
MOCK_API_RESPONSE_INVALID_TYPE = {
    "power": "2500",  # Should be number
    "powerAvg": 2400,
    "energyCounterIn": 30000,
}

# Typical device configuration
MOCK_DEVICE_CONFIG = {
    "ip_address": "192.168.1.100",
    "scan_interval": 60,
}

# Entry data for config entry
MOCK_ENTRY_DATA = {
    "ip_address": "192.168.1.100",
    "scan_interval": 60,
}

# Entry ID for tests
TEST_ENTRY_ID = "test_entry_id_12345"

# IP Address for tests
TEST_IP_ADDRESS = "192.168.1.100"

# API URL for tests
TEST_API_URL = f"http://{TEST_IP_ADDRESS}/v1/json"
