from __future__ import annotations

import math
import re

# Rough English average; a real tokenizer would replace this one function.
CHARS_PER_TOKEN = 4
_WORD = re.compile(r"\S+")


def estimate_tokens(text: str) -> int:
    """Conservative token estimate: the larger of a character- and a word-based guess."""
    if not text:
        return 0
    by_chars = math.ceil(len(text) / CHARS_PER_TOKEN)
    by_words = len(_WORD.findall(text))
    return max(by_chars, by_words)
