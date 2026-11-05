"""Local-only HTTP demonstration: bounded input, health, retries and safe logs."""

import argparse
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import monotonic
from uuid import uuid4

from agent_loader import create_agent
from reliability import retry


LOGGER = logging.getLogger("evidence_api")


class RateLimiter:
    """Single shared process bucket; deliberately not a production user quota."""

    def __init__(self, limit: int = 20, window: float = 60):
        self.limit = limit
        self.window = window
        self.requests = []

    def allow(self) -> bool:
        now = monotonic()
        self.requests = [stamp for stamp in self.requests if now - stamp < self.window]
        if len(self.requests) >= self.limit:
            return False
        self.requests.append(now)
        return True


def make_handler(agent=None):
    agent = agent if agent is not None else create_agent()
    limiter = RateLimiter()

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(5)

        def log_message(self, format, *args):
            # Do not log questions, evidence, request headers or arbitrary paths.
            pass

        def send_json(self, status: int, payload: dict):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Connection", "close")
            if status == 429:
                self.send_header("Retry-After", "60")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/health":
                self.send_json(200, {"status": "ok", "mode": "offline"})
            else:
                self.send_json(404, {"error": "Route not found"})

        def do_POST(self):
            request_id = uuid4().hex
            if self.path != "/ask":
                self.send_json(404, {"error": "Route not found"})
                return
            if not limiter.allow():
                self.send_json(429, {"error": "Too many requests"})
                return
            if self.headers.get("Transfer-Encoding"):
                self.send_json(400, {"error": "Transfer encoding is not supported"})
                return
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                self.send_json(415, {"error": "Use application/json"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self.send_json(400, {"error": "Invalid content length"})
                return
            if not 0 < length <= 8192:
                self.send_json(413, {"error": "Body must be 1-8192 bytes"})
                return
            start = monotonic()
            try:
                data = self.rfile.read(length)
                if len(data) != length:
                    raise ValueError("Incomplete request body.")
                payload = json.loads(data)
                if not isinstance(payload, dict) or set(payload) != {"question"}:
                    raise ValueError("Supply only a question field.")
                question = payload["question"]
                # Input validation lives in the shared evidence agent too.
                result = retry(lambda: agent.answer(question))
            except (ValueError, UnicodeError):
                self.send_json(400, {"error": "Supply a non-empty question of at most 2000 characters"})
                return
            except (TimeoutError, ConnectionError):
                self.send_json(503, {"error": "Service temporarily unavailable",
                                     "request_id": request_id})
                return
            except Exception:
                LOGGER.error("request_id=%s status=500", request_id)
                self.send_json(500, {"error": "Internal service error",
                                     "request_id": request_id})
                return
            LOGGER.info("request_id=%s status=200 latency_ms=%.2f",
                        request_id, (monotonic() - start) * 1000)
            self.send_json(200, {**result, "request_id": request_id})

    return Handler


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=["127.0.0.1", "0.0.0.0"], default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    server = HTTPServer((args.host, args.port), make_handler())
    print(f"Offline demo listening at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
