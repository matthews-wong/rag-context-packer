from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Chunk:
    """A retrieved passage. `score` is the retriever's relevance, higher is better."""

    id: str
    source: str
    text: str
    score: float


@dataclass(frozen=True)
class Dropped:
    id: str
    reason: str
    detail: str = ""


@dataclass(frozen=True)
class PackResult:
    selected: tuple[Chunk, ...]
    dropped: tuple[Dropped, ...]
    tokens_used: int
    budget_tokens: int
    notes: tuple[str, ...] = field(default=())
