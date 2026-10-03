from __future__ import annotations

from .similarity import jaccard, shingles
from .types import Chunk

DEFAULT_LAMBDA = 0.7


def mmr_order(chunks: list[Chunk], lambda_: float = DEFAULT_LAMBDA) -> list[Chunk]:
    """Order chunks by maximal marginal relevance.

    Each step picks the chunk maximising
    `lambda * relevance - (1 - lambda) * max_similarity_to_picked`.
    Scores are min-max normalised first so the trade-off does not depend on the
    retriever's score scale (BM25 scores are unbounded, cosine is not).
    """
    if not 0.0 <= lambda_ <= 1.0:
        raise ValueError(f"lambda_ must be within [0, 1], got {lambda_}")
    if not chunks:
        return []
    lo = min(c.score for c in chunks)
    hi = max(c.score for c in chunks)
    span = hi - lo
    relevance = {c.id: (c.score - lo) / span if span else 1.0 for c in chunks}
    sh = {c.id: shingles(c.text) for c in chunks}

    remaining = sorted(chunks, key=lambda c: -c.score)
    picked: list[Chunk] = []
    while remaining:
        def value(c: Chunk) -> float:
            redundancy = max((jaccard(sh[c.id], sh[p.id]) for p in picked), default=0.0)
            return lambda_ * relevance[c.id] - (1 - lambda_) * redundancy

        best = max(remaining, key=value)
        remaining.remove(best)
        picked.append(best)
    return picked
