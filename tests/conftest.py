"""Shared fixtures: run crews offline against a fake Anthropic API, so tests cost nothing."""

import json
import threading
from collections.abc import Callable, Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


class FakeAnthropic(ThreadingHTTPServer):
    """Minimal stand-in for the Anthropic Messages API.

    Records every POST /v1/messages body in `requests` and answers with `reply(body)`.
    Also answers /v1/messages/count_tokens, which CrewAI calls before each LLM call.
    """

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _MessagesHandler)
        self.reply: Callable[[dict], str] = lambda body: "ok"
        self.requests: list[dict] = []

    @property
    def url(self) -> str:
        host, port = self.server_address[:2]
        return f"http://{host}:{port}"


class _MessagesHandler(BaseHTTPRequestHandler):
    server: FakeAnthropic

    def do_POST(self) -> None:
        body = json.loads(self.rfile.read(int(self.headers["content-length"])))
        if self.path.startswith("/v1/messages/count_tokens"):
            response: dict = {"input_tokens": len(json.dumps(body)) // 4}
        else:
            self.server.requests.append(body)
            response = {
                "id": f"msg_{len(self.server.requests)}",
                "type": "message",
                "role": "assistant",
                "model": body["model"],
                "content": [{"type": "text", "text": self.server.reply(body)}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 10, "output_tokens": 5},
            }
        payload = json.dumps(response).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        pass  # keep test output clean


@pytest.fixture(autouse=True)
def offline_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use Claude with a dummy key, never reach the real API, and turn off CrewAI's network extras."""
    monkeypatch.setenv("MODEL", "anthropic/claude-opus-5-5")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:9")  # closed port: real calls fail fast
    monkeypatch.setenv("CREWAI_DISABLE_TELEMETRY", "true")
    monkeypatch.setenv("CREWAI_TRACING_ENABLED", "false")
    monkeypatch.setenv("CREWAI_DISABLE_VERSION_CHECK", "true")


@pytest.fixture
def fake_anthropic(monkeypatch: pytest.MonkeyPatch) -> Iterator[FakeAnthropic]:
    """Start a FakeAnthropic server and point the Anthropic SDK at it."""
    server = FakeAnthropic()
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setenv("ANTHROPIC_BASE_URL", server.url)
    # Reach the fake server directly, even when an HTTP proxy is configured.
    monkeypatch.setenv("NO_PROXY", "127.0.0.1")
    monkeypatch.setenv("no_proxy", "127.0.0.1")
    yield server
    server.shutdown()
    server.server_close()
