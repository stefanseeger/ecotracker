# Ecotracker Home Assistant Integration

Give me a tip: [paypal.me/StefanSeeger](https://www.paypal.com/paypalme/StefanSeeger) [buymeacoffee.com/stefsee](https://buymeacoffee.com/stefsee)

Custom integration for Ecotracker energy monitoring device. It directly accessed the local HTTP server. Depending on the [official API Specification](https://everhome.cloud/en/developer/ecotracker)

## Installation

### Prerequisites

1. Make sure your ecotracker and Home Assistant are in the same LAN/WIFI
1. Make sure your ecotracker has enabled "Local http server" of your Ecotacker device
  ![Local HTTP Server](docs/local_http_server.jpg)
1. Make sure your ecotracker is reachable in the local network via (http://your.local.ip.address/v1/json).
1. Make sure your calling http://your.local.ip.address/v1/json in the browser returns at least data like below. If one of the fields is missing, configuration will fail.
```json
{
   "power": 123, //mandatory
   "powerAvg": 456, //mandatory
   "energyCounterIn": 789 //mandatory
}
```

### HACS (Recommended)

1. Add this repository as a custom repository in HACS:
   - Go to HACS > Integrations
   - Click the three dots in the top right
   - Select "Custom repositories"
   - Add the repository URL and select "Integration" as the category
1. Click "Install"
1. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/ecotracker` folder to your Home Assistant's `custom_components` directory
1. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
1. Click "+ Add Integration"
1. Search for "Ecotracker"
1. Enter your device's IP address
1. Set the polling interval (default: 60 seconds, range: 1-86400 seconds)
1. Optionally set the **Power change threshold** in Watts (default: `0`, range: `0-1000`): suppresses small idle jitter below the threshold while still reporting larger changes immediately (and publishes a heartbeat on the first successful poll after 30 seconds; depends on the polling interval)
1. Optionally adjust per-sensor minimum update intervals (`0-86400` seconds, `0` = match polling interval):
   - Phase 1-3 power (default: `30 s`)
   - Power average (default: `60 s`)
   - Energy counters (default: `60 s`)
   - Diagnostic sensors — measurement age & Wi-Fi RSSI (default: `60 s`)

## Testing with the mock server

Start the local mock API server from the repository root:

```sh
python tests/ecotracker-mock-server.py
```

It serves a static JSON response containing all supported measurement fields at
`http://<host-ip>:8000/v1/json`. Enter that URL's host IP address in the
integration configuration. The server listens on all network interfaces and
uses port `8000` by default.

### Changing Settings

To change the polling interval, power change threshold, per-sensor update intervals, or IP address after setup:

1. Go to Settings > Devices & Services
1. Find your Ecotracker device
1. Click the three dots menu and select "Reconfigure"
1. Update any settings as needed

## Features

- Configurable polling interval (1-86400 seconds, default: 60 seconds)
- Optional power change threshold (deadband) to reduce database writes on fast polling intervals (e.g. 1 s) while keeping instant response to load changes
- Configurable per-sensor update throttling so high-frequency polling only writes secondary, energy, and diagnostic sensors as often as needed
- Compatible with Home Assistant Energy Dashboard
- Config flow UI for easy setup and reconfiguration without re-adding the integration

## Sensors

When polling faster than a sensor's configured minimum update interval, state writes to Home Assistant are throttled to keep the database compact (set any interval to `0` to match the polling interval; availability changes are always reported immediately):

- `sensor.ecotracker_power` - Current power consumption in Watts (updates at full polling interval; optional deadband publishes on the first successful poll after 30 s)
- `sensor.ecotracker_power_average` - Average power consumption (last minute, max once every 60 s)
- `sensor.ecotracker_energy_in` - Total energy imported in Watt-hours (max once every 60 s)
- `sensor.ecotracker_energy_in_t1` - Energy imported (1.8.1) in Watt-hours (max once every 60 s)
- `sensor.ecotracker_energy_in_t2` - Energy imported (1.8.2) in Watt-hours (max once every 60 s)
- `sensor.ecotracker_energy_out` - Total energy exported in Watt-hours (optional, max once every 60 s)
- `sensor.ecotracker_power_phase_1` - Power consumption of phase 1 in Watts (optional, max once every 30 s)
- `sensor.ecotracker_power_phase_2` - Power consumption of phase 2 in Watts (optional, max once every 30 s)
- `sensor.ecotracker_power_phase_3` - Power consumption of phase 3 in Watts (optional, max once every 30 s)
- `sensor.ecotracker_age_power` - Milliseconds since last measurement (diagnostic, disabled by default, max once every 60 s)
- `sensor.ecotracker_rssi` - Wi-Fi signal strength (diagnostic, disabled by default, max once every 60 s)
- `sensor.ecotracker_ssid` - Wi-Fi network name (diagnostic)
- `sensor.ecotracker_ip_address` - Configured IP address (diagnostic)
- `sensor.ecotracker_scan_interval` - Configured polling interval in seconds (diagnostic)

## 📝 Disclaimer

This software is not affiliated with, endorsed by, or associated with EcoTracker or everHome in any way. All product and brand names mentioned belong to their respective owners.
It is provided as-is, without any warranties or guarantees. The authors assume no liability for any issues arising from its use.
