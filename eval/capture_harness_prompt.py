"""Capture one model API request locally without forwarding it."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class CaptureHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        size = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(size))
        output = Path("first_request.json")
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

        messages = payload.get("messages", [])
        tools = payload.get("tools", [])
        print(f"Saved: {output.resolve()}")
        print(f"Endpoint: {self.path}")
        print(f"Top-level keys: {list(payload)}")
        print(f"Messages: {len(messages)}; tools: {len(tools)}")
        print(f"Roles: {[m.get('role') for m in messages]}")
        print(f"Tool names: {[t.get('function', t).get('name') for t in tools]}")

        response = b'{"error":{"message":"Captured locally; no upstream call"}}'
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


print("Capturing the next POST on http://127.0.0.1:8000")
HTTPServer(("127.0.0.1", 8000), CaptureHandler).handle_request()
