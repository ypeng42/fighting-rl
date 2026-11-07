"""Capture the first DeepSeek Harness model request and estimate its prompt size."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import tiktoken

ENCODING = tiktoken.get_encoding("o200k_base")
OUTPUT = Path("deepseek_first_request.json")


def as_text(value):
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def token_count(value):
    return len(ENCODING.encode(as_text(value)))


class CaptureHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.send_error(400, "Expected a JSON model request")
            return

        OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        messages = data.get("messages", [])
        if not isinstance(messages, list):
            messages = []
        tools = data.get("tools", [])
        if not isinstance(tools, list):
            tools = []

        lines = [
            f"Model: {data.get('model', '<not provided>')}",
            f"Endpoint: {self.path}",
            "Tokenizer: o200k_base (estimate, NOT exact DeepSeek billing tokens)",
            "",
            "Messages:",
        ]
        system_tokens = 0
        message_tokens = 0
        for index, message in enumerate(messages):
            role = message.get("role", "unknown")
            content = message.get("content", "")
            count = token_count(content)
            message_tokens += count
            if role in ("system", "developer"):
                system_tokens += count
            lines.append(f"  [{index}] {role:12s}: {count:>6} tokens | {len(as_text(content)):>7} characters")

        tool_tokens = token_count(tools) if tools else 0
        if tools:
            lines.append("")
            lines.append("Tools:")
            for index, tool in enumerate(tools):
                fn = tool.get("function", tool)
                name = fn.get("name", "unknown") if isinstance(fn, dict) else "unknown"
                lines.append(f"  [{index}] {name}: {token_count(tool)} tokens")
        lines.extend(
            [
                "",
                f"System/developer content: {system_tokens} tokens",
                f"All tool schemas (JSON): {tool_tokens} tokens",
                f"System/developer + tools: {system_tokens + tool_tokens} tokens",
                f"All message content + tools: {message_tokens + tool_tokens} tokens",
                "",
                "Caution: message-role framing, provider serialization, and model-specific",
                "tokenization are NOT counted. User-role runtime injections may also add",
                "harness tokens; inspect each user message rather than assuming it is task text.",
            ]
        )
        Path("deepseek_prompt_breakdown.txt").write_text("\n".join(lines) + "\n")
        Path("deepseek_tool_schemas.json").write_text(
            json.dumps(tools, indent=2, ensure_ascii=False)
        )
        Path("deepseek_system_prompt.txt").write_text(
            "\n\n".join(
                as_text(message.get("content", ""))
                for message in messages
                if message.get("role") in ("system", "developer")
            )
        )
        print("\n".join(lines), flush=True)
        print(f"\nSaved: {OUTPUT.resolve()}", flush=True)
        print("Also saved: deepseek_system_prompt.txt, deepseek_tool_schemas.json", flush=True)

        body = b'{"error":{"message":"Captured successfully; test server has no model."}}'
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


print("Listening on http://127.0.0.1:8000", flush=True)
print("Waiting for DeepSeek Harness to send its first model request...", flush=True)
HTTPServer(("127.0.0.1", 8000), CaptureHandler).handle_request()
