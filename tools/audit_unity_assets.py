#!/usr/bin/env python3
"""Audit Unity assets from an extracted WebGL bundle using UnityPy.

Usage:
  /usr/bin/python3 tools/audit_unity_assets.py \
    --input extracted/data/data.unity3d \
    --out-dir extracted/reports
"""

from __future__ import annotations

import argparse
from pathlib import Path

import UnityPy  # type: ignore


KEYWORDS = (
    "menu",
    "play",
    "start",
    "restart",
    "again",
    "score",
    "leader",
    "login",
    "credits",
    "gameover",
    "button",
    "ui",
    "canvas",
    "font",
)


def safe_name(obj_data) -> str:
    for attr in ("name", "m_Name"):
        if hasattr(obj_data, attr):
            value = getattr(obj_data, attr)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return "<unnamed>"


def matches_keywords(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in KEYWORDS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="extracted/reports")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    env = UnityPy.load(str(input_path))

    inventory_path = out_dir / "asset_inventory.txt"
    hits_path = out_dir / "menu_ui_hits.txt"

    counts: dict[str, int] = {}
    lines: list[str] = []
    hits: list[str] = []

    for obj in env.objects:
        t = obj.type.name
        counts[t] = counts.get(t, 0) + 1

        try:
            data = obj.read()
        except Exception as exc:
            line = f"{t}\t<read-error>\tpath_id={obj.path_id}\t{exc}"
            lines.append(line)
            continue

        name = safe_name(data)
        line = f"{t}\t{name}\tpath_id={obj.path_id}"
        lines.append(line)

        if matches_keywords(name):
            hits.append(line)

        if t == "TextAsset":
            text_content = ""
            try:
                script = getattr(data, "script", b"")
                if isinstance(script, bytes):
                    text_content = script.decode("utf-8", errors="ignore")
                else:
                    text_content = str(script)
            except Exception:
                text_content = ""
            if text_content and matches_keywords(text_content):
                preview = " ".join(text_content.split())[:220]
                hits.append(f"TextAssetContent\t{name}\tpath_id={obj.path_id}\t{preview}")

    summary = ["Asset counts by type:"]
    for k in sorted(counts):
        summary.append(f"- {k}: {counts[k]}")

    inventory_path.write_text("\n".join(summary + ["", "All objects:"] + lines), encoding="utf-8")
    hits_path.write_text("\n".join(hits) if hits else "No menu/UI keyword hits found.", encoding="utf-8")

    print(f"Wrote: {inventory_path}")
    print(f"Wrote: {hits_path}")
    print("Top-level counts:")
    for k in sorted(counts):
        print(f"  {k:20} {counts[k]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
