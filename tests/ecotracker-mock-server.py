"""Simple HTTP mock server for the Ecotracker JSON API."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

MOCK_RESPONSE = {
    "power": 2500,
    "powerAvg": 2400,
    "powerPhase1": 850,
    "powerPhase2": 800,
    "powerPhase3": 850,
    "energyCounterIn": 50000,
    "energyCounterInT1": 25000,
    "energyCounterInT2": 25000,
    "energyCounterOut": 5000,
    "agePower": 5000,
    "rssi": -50,
    "ssid": "Ecotracker-Mock",
}


class EcotrackerMockHandler(BaseHTTPRequestHandler):
    """Serve a static Ecotracker API response."""

    def do_GET(self) -> None:
        """Return mock data for the API endpoint."""
        if self.path in ("/", "/v1"):
            response = b"Use /v1/json to retrieve the Ecotracker mock data."
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            return

        if self.path != "/v1/json":
            self.send_error(404)
            return

        response = json.dumps(MOCK_RESPONSE).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), EcotrackerMockHandler)
    print("Ecotracker mock server listening on http://0.0.0.0:8000/v1/json")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Ecotracker mock server")
        server.server_close()
