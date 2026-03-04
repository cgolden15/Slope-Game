#!/usr/bin/env python3
"""Apply UI text replacements to IL2CPP global-metadata.dat safely.

Requirements:
- Replacement is byte-preserving by slot: len(to_utf8) <= len(from_utf8)
- The script pads with spaces to keep binary offsets stable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    config_path = Path(args.config)
    out_path = Path(args.output)

    blob = metadata_path.read_bytes()
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    replacements = cfg.get("replacements", [])

    applied = 0
    skipped = 0

    for item in replacements:
        src = item.get("from", "")
        dst = item.get("to", "")

        if not isinstance(src, str) or not isinstance(dst, str) or not src:
            skipped += 1
            continue

        src_b = src.encode("utf-8")
        dst_b = dst.encode("utf-8")

        if len(dst_b) > len(src_b):
            skipped += 1
            continue

        if src_b == dst_b:
            continue

        padded = dst_b + (b" " * (len(src_b) - len(dst_b)))
        count = blob.count(src_b)
        if count == 0:
            skipped += 1
            continue

        blob = blob.replace(src_b, padded)
        applied += count

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(blob)

    print(f"Applied replacements (occurrences): {applied}")
    print(f"Skipped entries: {skipped}")
    print(f"Wrote metadata: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
