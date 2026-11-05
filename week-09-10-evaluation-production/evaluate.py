"""Deterministic local baseline. No LLM judge, paid APIs or fabricated token counts."""

import argparse
import json
from pathlib import Path
from statistics import mean
from time import perf_counter

from agent_loader import create_agent


DATASET = Path(__file__).with_name("evaluation_cases.json")


def evaluate(cases: list[dict]) -> dict:
    if not cases:
        raise ValueError("Evaluation dataset must not be empty.")
    agent = create_agent()
    results = []
    for case in cases:
        start = perf_counter()
        response = agent.answer(case["question"])
        elapsed = (perf_counter() - start) * 1000
        hits = agent.search(case["question"])
        sources = [citation["source"] for citation in response["citations"]]
        status_ok = response["status"] == case["status"]
        citation_ok = (case["source"] in sources if case["source"] else not sources)
        content_ok = (
            case["contains"].lower() in response["answer"].lower()
            if case["contains"] else True
        )
        results.append({
            "id": case["id"], "question": case["question"],
            "passed": status_ok and citation_ok and content_ok,
            "retrieval_hit": any(hit["source"] == case["source"] for hit in hits),
            "expected_source": case["source"], "actual_sources": sources,
            "expected_status": case["status"], "actual_status": response["status"],
            "latency_ms": round(elapsed, 3),
        })
    supported = [row for row in results if row["expected_source"]]
    unknown = [row for row in results if not row["expected_source"]]
    latencies = sorted(row["latency_ms"] for row in results)
    return {
        "baseline": "v1-offline-tfidf-extractive",
        "case_count": len(results),
        "pass_rate": mean(row["passed"] for row in results),
        "retrieval_recall_at_2": (
            mean(row["retrieval_hit"] for row in supported) if supported else None
        ),
        "unknown_abstention_rate": (
            mean(row["actual_status"] == "insufficient_evidence" for row in unknown)
            if unknown else None
        ),
        "latency_mean_ms": round(mean(latencies), 3),
        "latency_p95_ms": latencies[max(0, (95 * len(latencies) + 99) // 100 - 1)],
        "llm_tokens": None,
        "api_cost_usd": 0,
        "tool_selection_accuracy": None,
        "notes": "No LLM or model-selected tools. Keyword checks are not semantic correctness.",
        "failures": [row for row in results if not row["passed"]],
        "results": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true", help="Fail below the v1 90 percent floor")
    args = parser.parse_args()
    report = evaluate(json.loads(DATASET.read_text(encoding="utf-8")))
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if args.check and report["pass_rate"] < 0.90:
        raise SystemExit(1)
