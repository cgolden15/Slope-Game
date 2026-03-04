#!/usr/bin/env python3
"""Apply many texture overrides in one pass to a Unity bundle.

Config JSON format:
{
  "bundle": "extracted/data/data.unity3d",
  "output_bundle": "extracted/data/data.modified.unity3d",
  "overrides": [
    { "target": "slope_icon", "png": "extracted/branding-overrides/slope_icon.png" }
  ]
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import UnityPy  # type: ignore
from PIL import Image


def get_obj_name(data) -> str:
    for attr in ("name", "m_Name"):
        if hasattr(data, attr):
            value = getattr(data, attr)
            if isinstance(value, str):
                return value
    return ""


def save_environment(env, output_path: Path) -> None:
    if hasattr(env, "file") and hasattr(env.file, "save"):
        output_path.write_bytes(env.file.save())
        return
    if hasattr(env, "save"):
        output_path.write_bytes(env.save())
        return
    for _name, file_obj in env.files.items():
        if hasattr(file_obj, "save"):
            output_path.write_bytes(file_obj.save())
            return
    raise RuntimeError("Could not determine how to save modified Unity environment")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config_path = Path(args.config)
    root = config_path.resolve().parents[1]
    cfg = json.loads(config_path.read_text(encoding="utf-8"))

    bundle_path = root / cfg["bundle"]
    output_path = root / cfg["output_bundle"]
    overrides = cfg.get("overrides", [])

    env = UnityPy.load(str(bundle_path))

    replacement_images: dict[str, Image.Image] = {}
    for item in overrides:
        target = item["target"]
        png_path = root / item["png"]
        if not png_path.exists():
            continue
        replacement_images[target] = Image.open(png_path).convert("RGBA")

    if not replacement_images:
        raise RuntimeError("No override PNGs found to apply")

    counts = {k: 0 for k in replacement_images}

    for obj in env.objects:
        if obj.type.name not in {"Texture2D", "Sprite"}:
            continue

        data = obj.read()
        name = get_obj_name(data)
        if name not in replacement_images:
            continue

        replacement = replacement_images[name]
        if obj.type.name == "Texture2D":
            data.image = replacement
            data.save()
            counts[name] += 1
        elif hasattr(data, "image"):
            try:
                data.image = replacement
                data.save()
                counts[name] += 1
            except Exception:
                # Some Sprite image accessors are read-only in UnityPy.
                # Matching Texture2D replacements still update the rendered sprite.
                continue

    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_environment(env, output_path)

    replaced_total = sum(counts.values())
    print(f"Total replaced objects: {replaced_total}")
    for key in sorted(counts):
        if counts[key] > 0:
            print(f"- {key}: {counts[key]}")
    print(f"Wrote modified bundle: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
