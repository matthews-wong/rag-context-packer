from __future__ import annotations

import argparse
import json
import sys

from .pack import pack
from .render import render_context
from .types import Chunk


def load_chunks(raw: str) -> list[Chunk]:
    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"input is not valid JSON: {exc}")
    if not isinstance(items, list):
        raise SystemExit("input must be a JSON array of {id, source, text, score}")
    chunks = []
    for i, item in enumerate(items):
        try:
            chunks.append(Chunk(str(item["id"]), str(item["source"]), str(item["text"]), float(item["score"])))
        except (KeyError, TypeError, ValueError) as exc:
            raise SystemExit(f"item {i} is malformed ({exc!r}); need id, source, text, numeric score")
    return chunks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="context_packer", description="Pack scored chunks into a token budget.")
    parser.add_argument("file", nargs="?", help="JSON file of chunks (default: stdin)")
    parser.add_argument("--budget", type=int, required=True, help="token budget for the packed context")
    parser.add_argument("--json", action="store_true", help="print the selection report as JSON")
    args = parser.parse_args(argv)

    raw = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    try:
        result = pack(load_chunks(raw), args.budget)
    except ValueError as exc:
        raise SystemExit(str(exc))

    if args.json:
        report = {
            "selected": [c.id for c in result.selected],
            "dropped": [{"id": d.id, "reason": d.reason, "detail": d.detail} for d in result.dropped],
            "tokens_used": result.tokens_used,
            "budget_tokens": result.budget_tokens,
        }
        print(json.dumps(report, indent=2))
    else:
        print(render_context(result.selected))
        print(f"\n[{result.tokens_used}/{result.budget_tokens} tokens, {len(result.dropped)} dropped]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
