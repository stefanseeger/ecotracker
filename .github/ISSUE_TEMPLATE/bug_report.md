---
name: Bug report
about: Report a bug in the Ecotracker Home Assistant integration
labels: bug
---

Hi, thanks for reaching out.
Please follow the instructions below.

You can open your ticket in German or English.
# Before you open the ticket
1. Make sure your ecotracker and Home Assistant are in the same LAN/WIFI
1. Make sure your ecotracker has enabled "Local http server" of your Ecotacker device
  ![Local HTTP Server](../../docs/local_http_server.jpg)
1. Make sure your ecotracker is reachable in the local network via (http://your.local.ip.address/v1/json).
1. Make sure your calling http://your.local.ip.address/v1/json in the browser returns at least data like below. If one of the fields is missing, configuration will fail.
```json
{
    "power": 123, //mandatory
    "powerAvg": 456, //mandatory
    "energyCounterIn": 789 //mandatory
}
```

# Output of http://your.local.ip.address/v1/json
To help you debug I need the JSON output

```json
{
    // FILL HERE
}
```

# Bug description
[Explain your problem here]

