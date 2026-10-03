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

## CLI

```
python3 -m context_packer fixtures/chunks.json --budget 60          # rendered context
python3 -m context_packer fixtures/chunks.json --budget 30 --json   # selection report
```

Input is a JSON array of `{id, source, text, score}`. The rendered output
wraps each chunk in a `<document id=... source=...>` element, escapes `<` in
chunk text so a document cannot close its own wrapper, and prefixes a notice
that the content is untrusted.

## Design notes

- Tokens are estimated (`max(chars / 4, words)`), not counted. Pass
  `count_tokens=` to `pack` to plug in a real tokenizer.
- MMR runs on min-max normalised scores, so `lambda_` means the same thing
  for BM25 and for cosine scores.
- Similarity is word-trigram Jaccard: cheap, deterministic, and good at
  catching copies, not paraphrases.

## Fixture eval

```
PYTHONPATH=. python3 scripts/eval_redundancy.py
```

On the 4-chunk fixture with a 60-token budget, plain top-k fits 2 chunks
covering 1 distinct fact; the packer fits 3 chunks covering 3. The fixture is
hand-made to show the mechanism; it is not a benchmark.

## Tests

```
python3 -m unittest discover -s tests -v
```
