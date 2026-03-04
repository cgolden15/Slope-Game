#!/usr/bin/env python3
"""Export editable UI text candidates from IL2CPP global-metadata.dat.

This creates a JSON file with string replacements you can edit safely.
Only replacements with equal-or-shorter byte length are allowed when applying.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_KEYWORDS = [
    "slope",
    "leader",
    "score",
    "high",
    "best",
    "recent",
    "play",
    "login",
    "register",
    "again",
    "retry",
    "restart",
    "menu",
    "game",
    "name",
    "credits",
    "sound",
    "speed",
]


def printable_ratio(s: str) -> float:
    if not s:
        return 0.0
    printable = sum(1 for ch in s if ch.isprintable())
    return printable / len(s)


def extract_null_terminated_strings(blob: bytes, min_len: int = 3) -> list[str]:
    out: list[str] = []
    for part in blob.split(b"\x00"):
        if len(part) < min_len:
            continue
        try:
            s = part.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if printable_ratio(s) < 0.92:
            continue
        out.append(s)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--keywords", nargs="*", default=DEFAULT_KEYWORDS)
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    out_path = Path(args.output)

    blob = metadata_path.read_bytes()
    strings = extract_null_terminated_strings(blob)

    keywords = [k.lower() for k in args.keywords]
    selected = []
    seen = set()
    for s in strings:
        ls = s.lower()
        if any(k in ls for k in keywords):
            if s in seen:
                continue
            seen.add(s)
            selected.append(
                {
                    "from": s,
                    "to": s,
                    "maxBytes": len(s.encode("utf-8")),
                }
            )

    payload = {
        "metadata": str(metadata_path),
        "note": "Edit values in 'to'. Keep UTF-8 byte length <= maxBytes.",
        "replacements": selected,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported candidates: {len(selected)}")
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
