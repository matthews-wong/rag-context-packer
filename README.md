# rag-context-packer

Retrieval gives you a ranked list of chunks; the prompt only has room for some
of them. This library decides which ones go in. It takes scored chunks and a
token budget and returns a selection that:

- drops near-duplicate chunks (the same paragraph indexed from two files),
- spreads the selection across the material with maximal marginal relevance,
- never cuts a chunk in half: a chunk that does not fit is skipped, and a
  smaller, lower-ranked one may still take the remaining room,
- reports what was dropped and why, so a missing citation is explainable.

Pure standard-library Python 3.12, no model, no network.

## Usage

```python
from context_packer import Chunk, pack

chunks = [
    Chunk(id="ops.md#3", source="ops.md", text="Rotate the key every 90 days.", score=0.91),
    Chunk(id="faq.md#1", source="faq.md", text="Rotate the key every 90 days!", score=0.88),
]
result = pack(chunks, budget_tokens=400)
print([c.id for c in result.selected])   # ['ops.md#3']
print(result.dropped)                    # [Dropped(id='faq.md#1', reason='duplicate', ...)]
```

## Tests

```
python3 -m unittest discover -s tests -v
```
