"""Local workflow history. Not a multi-user conversation database."""

import json
from pathlib import Path
import tempfile


DEFAULT_STATE = Path(__file__).resolve().parent / ".state" / "history.json"


class StateStore:
    def __init__(self, path: Path = DEFAULT_STATE):
        self.path = Path(path)

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            history = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeError) as error:
            raise ValueError("History is damaged; choose another state file.") from error
        if not isinstance(history, list) or any(
            not isinstance(item, dict)
            or not isinstance(item.get("question"), str)
            or not isinstance(item.get("result"), dict)
            for item in history
        ):
            raise ValueError("History must contain question/result records.")
        return history

    def append(self, question: str, result: dict) -> None:
        history = self.load()
        history.append({"question": question, "result": result})
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Replace atomically so an interrupted write does not truncate history.
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=self.path.parent,
            suffix=".tmp", delete=False
        ) as handle:
            temporary = Path(handle.name)
            json.dump(history[-50:], handle, indent=2, ensure_ascii=False)
        try:
            temporary.replace(self.path)
        finally:
            temporary.unlink(missing_ok=True)
