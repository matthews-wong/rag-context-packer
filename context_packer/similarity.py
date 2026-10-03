from __future__ import annotations

import re

_WORD = re.compile(r"[a-z0-9]+")
SHINGLE_SIZE = 3


def shingles(text: str, size: int = SHINGLE_SIZE) -> frozenset[tuple[str, ...]]:
    """Word n-grams, lower-cased and stripped of punctuation.

    Texts shorter than `size` words fall back to unigrams so short chunks
    still compare meaningfully.
    """
    words = _WORD.findall(text.lower())
    if len(words) < size:
        return frozenset((w,) for w in words)
    return frozenset(tuple(words[i : i + size]) for i in range(len(words) - size + 1))


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a and not b:
        return 1.0
    union = len(a | b)
    return len(a & b) / union if union else 0.0
