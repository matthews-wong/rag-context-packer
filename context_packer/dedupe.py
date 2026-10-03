from __future__ import annotations

from .similarity import jaccard, shingles
from .types import Chunk, Dropped

DEFAULT_DUPLICATE_THRESHOLD = 0.8


def drop_duplicates(
    chunks: list[Chunk], threshold: float = DEFAULT_DUPLICATE_THRESHOLD
) -> tuple[list[Chunk], list[Dropped]]:
    """Keep the highest-scoring chunk of each near-duplicate group.

    Chunks are visited best-first so the survivor is always the better-scored
    copy, regardless of input order. Ties keep the earlier input position.
    """
    kept: list[Chunk] = []
    kept_shingles = []
    dropped: list[Dropped] = []
    for chunk in sorted(chunks, key=lambda c: -c.score):
        sh = shingles(chunk.text)
        twin = next(
            (k for k, ks in zip(kept, kept_shingles) if jaccard(sh, ks) >= threshold),
            None,
        )
        if twin is None:
            kept.append(chunk)
            kept_shingles.append(sh)
        else:
            dropped.append(Dropped(chunk.id, "duplicate", f"near-copy of {twin.id}"))
    return kept, dropped
