from contextlib import contextmanager
import http.client
from http.server import HTTPServer
import json
from pathlib import Path
import subprocess
import sys
import threading
import unittest
from unittest.mock import Mock

from evaluate import DATASET, evaluate
from main import make_handler, RateLimiter
from reliability import retry


@contextmanager
def running_server(agent=None):
    server = HTTPServer(("127.0.0.1", 0), make_handler(agent))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_address[1]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def request(port, method="POST", body=None, path="/ask", content_type="application/json"):
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        connection.request(method, path, body=body,
                           headers={"Content-Type": content_type})
        response = connection.getresponse()
        return response.status, json.loads(response.read())
    finally:
        connection.close()


class ApiTests(unittest.TestCase):
    def test_answer_and_health(self):
        with running_server() as port:
            status, result = request(port, body=json.dumps({"question": "FastAPI?"}))
            self.assertEqual(status, 200)
            self.assertEqual(result["citations"][0]["source"], "fastapi.md")
            self.assertEqual(len(result["request_id"]), 32)
            self.assertEqual(request(port, method="GET", path="/health"),
                             (200, {"status": "ok", "mode": "offline"}))

    def test_invalid_bodies_and_limits(self):
        with running_server() as port:
            bodies = ["broken", "[]", "{}", '{"question": 7}',
                      '{"question": ""}', '{"question": "x", "extra": 1}',
                      json.dumps({"question": "x" * 2001})]
            for body in bodies:
                with self.subTest(body=body[:40]):
                    self.assertEqual(request(port, body=body)[0], 400)
            self.assertEqual(request(port, body="x" * 8193)[0], 413)
            self.assertEqual(request(port, body="x", content_type="text/plain")[0], 415)
            self.assertEqual(request(port, body="{}", path="/unknown")[0], 404)

    def test_unknown_question_abstains(self):
        with running_server() as port:
            status, result = request(port, body='{"question": "Who wrote Hamlet?"}')
            self.assertEqual(status, 200)
            self.assertEqual(result["status"], "insufficient_evidence")

    def test_http_rate_limit(self):
        with running_server() as port:
            for _ in range(20):
                self.assertEqual(request(port, body='{"question": "FastAPI?"}')[0], 200)
            self.assertEqual(request(port, body='{"question": "FastAPI?"}')[0], 429)
            self.assertEqual(request(port, method="GET", path="/health")[0], 200)

    def test_transient_failure_returns_503_after_three_attempts(self):
        agent = Mock()
        agent.answer.side_effect = TimeoutError("private backend detail")
        with running_server(agent) as port:
            status, body = request(port, body='{"question": "FastAPI?"}')
        self.assertEqual(status, 503)
        self.assertNotIn("private", json.dumps(body))
        self.assertEqual(agent.answer.call_count, 3)

    def test_unexpected_failure_does_not_leak_details(self):
        agent = Mock()
        agent.answer.side_effect = RuntimeError("private backend detail")
        with running_server(agent) as port:
            status, body = request(port, body='{"question": "FastAPI?"}')
        self.assertEqual(status, 500)
        self.assertNotIn("private", json.dumps(body))
        self.assertEqual(agent.answer.call_count, 1)


class ReliabilityTests(unittest.TestCase):
    def test_backoff_and_success(self):
        operation = Mock(side_effect=[TimeoutError(), ConnectionError(), "ok"])
        sleep = Mock()
        self.assertEqual(retry(operation, sleep=sleep), "ok")
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [0.1, 0.2])

    def test_permanent_error_is_not_retried(self):
        operation = Mock(side_effect=ValueError("bad input"))
        with self.assertRaises(ValueError):
            retry(operation)
        self.assertEqual(operation.call_count, 1)

    def test_retry_bound(self):
        with self.assertRaises(ValueError):
            retry(lambda: None, attempts=4)

    def test_rate_limit_window_expires(self):
        limiter = RateLimiter(limit=1, window=0)
        self.assertTrue(limiter.allow())
        self.assertTrue(limiter.allow())


class EvaluationTests(unittest.TestCase):
    def test_dataset_and_baseline_gate(self):
        cases = json.loads(DATASET.read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 40)
        self.assertEqual(len({case["id"] for case in cases}), 40)
        report = evaluate(cases)
        self.assertGreaterEqual(report["pass_rate"], 0.90)
        self.assertEqual(report["api_cost_usd"], 0)
        self.assertIsNone(report["llm_tokens"])
        self.assertEqual(report["unknown_abstention_rate"], 1)
        self.assertTrue(all(row["latency_ms"] >= 0 for row in report["results"]))

    def test_evaluation_detects_a_wrong_expected_source(self):
        report = evaluate([{
            "id": "deliberate-failure", "question": "FastAPI?",
            "status": "answered", "source": "wrong.md", "contains": "FastAPI"
        }])
        self.assertEqual(report["pass_rate"], 0)
        self.assertEqual(len(report["failures"]), 1)

    def test_empty_dataset_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([])

    def test_evaluation_cli_help_regression(self):
        result = subprocess.run(
            [sys.executable, "-B", str(Path(__file__).with_name("evaluate.py")), "--help"],
            capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--check", result.stdout)


if __name__ == "__main__":
    unittest.main()
