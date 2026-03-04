#!/usr/bin/env python3
"""Export likely UI/menu assets from a Unity bundle to editable files.

Usage:
  /usr/bin/python3 tools/export_unity_ui_assets.py \
    --input extracted/data/data.unity3d \
    --out-dir extracted/ui-assets
"""

from __future__ import annotations

import argparse
import re
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
    "panel",
    "ui",
    "canvas",
    "font",
)


def clean_filename(name: str) -> str:
    name = name.strip() or "unnamed"
    name = re.sub(r"[^a-zA-Z0-9._-]+", "_", name)
    return name[:120]


def match_name(name: str) -> bool:
    n = name.lower()
    return any(k in n for k in KEYWORDS)


def get_name(obj_data) -> str:
    for attr in ("name", "m_Name"):
        if hasattr(obj_data, attr):
            val = getattr(obj_data, attr)
            if isinstance(val, str) and val.strip():
                return val.strip()
    return "unnamed"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="extracted/ui-assets")
    parser.add_argument("--export-all-textures", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    env = UnityPy.load(str(input_path))

    exported = 0
    skipped = 0

    for obj in env.objects:
        t = obj.type.name
        if t not in {"Sprite", "Texture2D", "Font", "TextAsset"}:
            continue

        try:
            data = obj.read()
        except Exception:
            skipped += 1
            continue

        name = get_name(data)
        should_export = args.export_all_textures if t in {"Sprite", "Texture2D"} else True
        if not should_export:
            should_export = match_name(name)

        if t == "TextAsset" and not should_export:
            try:
                content = data.script.decode("utf-8", errors="ignore") if isinstance(data.script, bytes) else str(data.script)
                should_export = any(k in content.lower() for k in KEYWORDS)
            except Exception:
                should_export = False

        if not should_export:
            skipped += 1
            continue

        base = f"{t}_{clean_filename(name)}_{obj.path_id}"
        if t in {"Sprite", "Texture2D"}:
            try:
                img = data.image
                target = out_dir / f"{base}.png"
                img.save(target)
                exported += 1
            except Exception:
                skipped += 1
                continue
        elif t == "Font":
            # Some fonts embed bytes in m_FontData
            font_data = getattr(data, "m_FontData", b"")
            if isinstance(font_data, (bytes, bytearray)) and len(font_data) > 0:
                # try guess extension
                ext = ".ttf" if font_data[:4] in (b"\x00\x01\x00\x00", b"OTTO") else ".bin"
                target = out_dir / f"{base}{ext}"
                target.write_bytes(bytes(font_data))
                exported += 1
            else:
                skipped += 1
        elif t == "TextAsset":
            script = getattr(data, "script", b"")
            if isinstance(script, bytes):
                text = script.decode("utf-8", errors="ignore")
            else:
                text = str(script)
            target = out_dir / f"{base}.txt"
            target.write_text(text, encoding="utf-8")
            exported += 1

    print(f"Exported files: {exported}")
    print(f"Skipped objects: {skipped}")
    print(f"Output folder : {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
