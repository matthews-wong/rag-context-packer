"""Compare plain top-k packing with the packer on the checked-in fixture.

Reports, for the same token budget, how many distinct facts reach the prompt.
The fixture is tiny and hand-made, so the numbers illustrate the mechanism
and are not a benchmark.
"""
from __future__ import annotations

import json
from pathlib import Path

from context_packer import Chunk, estimate_tokens, pack

ROOT = Path(__file__).resolve().parent.parent
BUDGET = 60
# Which fact each fixture chunk states; duplicates share a fact.
FACTS = {
    "runbook.md#4": "key-rotation",
    "faq.md#2": "key-rotation",
    "oncall.md#1": "escalation",
    "notes.md#9": "injection",
}


def naive_top_k(chunks: list[Chunk], budget: int) -> list[Chunk]:
    picked, used = [], 0
    for c in sorted(chunks, key=lambda c: -c.score):
        cost = estimate_tokens(c.text)
        if used + cost > budget:
            break
        picked.append(c)
        used += cost
    return picked


def main() -> None:
    raw = json.loads((ROOT / "fixtures" / "chunks.json").read_text(encoding="utf-8"))
    chunks = [Chunk(r["id"], r["source"], r["text"], r["score"]) for r in raw]
    naive = naive_top_k(chunks, BUDGET)
    packed = list(pack(chunks, BUDGET).selected)
    print(f"fixture: {len(chunks)} chunks, budget {BUDGET} tokens")
    print(f"{'strategy':<10} {'chunks':>6} {'distinct facts':>15}")
    for name, sel in (("top-k", naive), ("packer", packed)):
        print(f"{name:<10} {len(sel):>6} {len({FACTS[c.id] for c in sel}):>15}")


if __name__ == "__main__":
    main()
