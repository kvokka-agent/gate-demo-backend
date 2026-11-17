"""Minimal greeting API for the review-gate demo."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


FRONTEND_ORIGIN = "http://127.0.0.1:8000"


class GreetingHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", FRONTEND_ORIGIN)
        self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", FRONTEND_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "600")
        self.send_header("Vary", "Origin")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        if self.path != "/greet":
            self._send_json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", ""))
            if length < 0:
                raise ValueError("negative content length")
            request = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "Request must be valid JSON"})
            return

        if not isinstance(request, dict) or not isinstance(request.get("name"), str):
            self._send_json(400, {"error": "Request must include a string name"})
            return

        self._send_json(200, {"greeting": f"Hello, {request['name']}!"})


if __name__ == "__main__":
    print("Greeting backend listening at http://127.0.0.1:8001", flush=True)
    HTTPServer(("127.0.0.1", 8001), GreetingHandler).serve_forever()
