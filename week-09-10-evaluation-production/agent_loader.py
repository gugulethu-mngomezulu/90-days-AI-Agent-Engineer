"""Reuse Week 7's original implementation instead of duplicating it."""

from pathlib import Path
import sys

WEEK_7 = Path(__file__).resolve().parent.parent / "week-07-08-rag-mcp-state"
# Keep this week's main.py ahead of Week 7's CLI module.
sys.path.append(str(WEEK_7))

from evidence import EvidenceAgent  # noqa: E402


def create_agent() -> EvidenceAgent:
    return EvidenceAgent()
