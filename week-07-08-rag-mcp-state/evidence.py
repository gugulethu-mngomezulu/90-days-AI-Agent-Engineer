"""Offline retrieval baseline: TF-IDF vectors, cosine search, quoted evidence."""

from collections import Counter
from dataclasses import asdict, dataclass
import math
from pathlib import Path
import re


DATA_DIR = Path(__file__).resolve().parent / "data"
STOP_WORDS = set("a an the is are of to and in for how what does do can with my".split())


def tokens(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", text.lower())
            if word not in STOP_WORDS]


@dataclass(frozen=True)
class Chunk:
    source: str
    chunk_id: int
    text: str


def load_chunks(directory: Path = DATA_DIR, size: int = 40,
                overlap: int = 8) -> list[Chunk]:
    if size < 1 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size.")
    chunks = []
    for path in sorted(directory.glob("*.md")):
        words = path.read_text(encoding="utf-8").split()
        for index, start in enumerate(range(0, len(words), size - overlap)):
            chunks.append(Chunk(path.name, index, " ".join(words[start:start + size])))
            if start + size >= len(words):
                break
    return chunks


class EvidenceAgent:
    def __init__(self, chunks: list[Chunk] | None = None):
        self.chunks = load_chunks() if chunks is None else chunks
        counts = [Counter(tokens(chunk.text)) for chunk in self.chunks]
        vocabulary = {word for count in counts for word in count}
        self.idf = {
            word: math.log((1 + len(counts)) /
                           (1 + sum(word in count for count in counts))) + 1
            for word in vocabulary
        }
        self.vectors = [self._vector(count) for count in counts]

    def _vector(self, counts: Counter) -> dict[str, float]:
        vector = {word: count * self.idf[word]
                  for word, count in counts.items() if word in self.idf}
        norm = math.sqrt(sum(value * value for value in vector.values()))
        return {word: value / norm for word, value in vector.items()} if norm else {}

    def search(self, question: str, top_k: int = 2,
               min_score: float = 0.15) -> list[dict]:
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question must not be empty.")
        if len(question) > 2000:
            raise ValueError("Question must be at most 2000 characters.")
        if type(top_k) is not int or not 1 <= top_k <= 5:
            raise ValueError("top_k must be between 1 and 5.")
        if not 0 < min_score <= 1:
            raise ValueError("min_score must be greater than 0 and at most 1.")
        query = self._vector(Counter(tokens(question)))
        scored = []
        for chunk, vector in zip(self.chunks, self.vectors):
            score = sum(value * vector.get(word, 0) for word, value in query.items())
            if score >= min_score:
                scored.append({**asdict(chunk), "score": round(score, 4)})
        return sorted(scored, key=lambda hit: hit["score"], reverse=True)[:top_k]

    def answer(self, question: str) -> dict:
        hits = self.search(question)
        if not hits:
            return {
                "status": "insufficient_evidence",
                "answer": "I do not have enough evidence in the local documents.",
                "citations": [],
            }
        # Quoting avoids inventing facts; relevance still needs human evaluation.
        best = hits[0]
        return {
            "status": "answered",
            "answer": best["text"],
            "citations": [{"source": best["source"], "chunk_id": best["chunk_id"]}],
        }
