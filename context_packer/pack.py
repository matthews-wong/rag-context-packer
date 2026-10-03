from __future__ import annotations

from collections.abc import Callable

from .dedupe import DEFAULT_DUPLICATE_THRESHOLD, drop_duplicates
from .mmr import DEFAULT_LAMBDA, mmr_order
from .tokens import estimate_tokens
from .types import Chunk, Dropped, PackResult


def pack(
    chunks: list[Chunk],
    budget_tokens: int,
    *,
    duplicate_threshold: float = DEFAULT_DUPLICATE_THRESHOLD,
    lambda_: float = DEFAULT_LAMBDA,
    count_tokens: Callable[[str], int] = estimate_tokens,
) -> PackResult:
    """Select chunks that fit `budget_tokens`, whole or not at all.

    A chunk that does not fit is skipped rather than truncated, because a
    sentence cut mid-claim is worse evidence than no sentence. Later, smaller
    chunks may still use the remaining room.
    """
    if budget_tokens < 0:
        raise ValueError(f"budget_tokens must be >= 0, got {budget_tokens}")
    ids = [c.id for c in chunks]
    repeated = sorted({i for i in ids if ids.count(i) > 1})
    if repeated:
        raise ValueError(f"chunk ids must be unique, repeated: {', '.join(repeated)}")

    unique, dropped = drop_duplicates(chunks, duplicate_threshold)
    selected: list[Chunk] = []
    used = 0
    for chunk in mmr_order(unique, lambda_):
        cost = count_tokens(chunk.text)
        if used + cost > budget_tokens:
            dropped.append(
                Dropped(chunk.id, "over_budget", f"needs {cost}, {budget_tokens - used} left")
            )
            continue
        selected.append(chunk)
        used += cost
    return PackResult(tuple(selected), tuple(dropped), used, budget_tokens)
