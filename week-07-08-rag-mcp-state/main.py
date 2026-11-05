"""Run from this folder: python main.py --question "What is FastAPI?"."""

import argparse
import json
from pathlib import Path

from evidence import EvidenceAgent
from state_store import DEFAULT_STATE, StateStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline document evidence assistant")
    parser.add_argument("--question", default="What is FastAPI?")
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    args = parser.parse_args()
    store = StateStore(args.state)
    try:
        if args.history:
            output = store.load()
        else:
            output = EvidenceAgent().answer(args.question)
            store.append(args.question, output)
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
