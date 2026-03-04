#!/usr/bin/env python3
"""Replace a Texture2D or Sprite image by object name inside a Unity bundle.

Usage:
  /usr/bin/python3 tools/replace_texture_in_bundle.py \
    --bundle extracted/data/data.unity3d \
    --target-name loginBut \
    --png extracted/ui-assets/Texture2D_loginBut_5.png \
    --output extracted/data/data.modified.unity3d
"""

from __future__ import annotations

import argparse
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
    # UnityPy save API differs by version/object type.
    if hasattr(env, "file") and hasattr(env.file, "save"):
        output_path.write_bytes(env.file.save())
        return

    if hasattr(env, "save"):
        output_path.write_bytes(env.save())
        return

    # Fallback: first file in env.files
    for _name, file_obj in env.files.items():
        if hasattr(file_obj, "save"):
            output_path.write_bytes(file_obj.save())
            return

    raise RuntimeError("Could not determine how to save modified Unity environment")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--target-name", required=True, help="Exact object name of Texture2D/Sprite")
    parser.add_argument("--png", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    bundle_path = Path(args.bundle)
    output_path = Path(args.output)
    replacement_img = Image.open(args.png).convert("RGBA")

    env = UnityPy.load(str(bundle_path))

    replaced = 0
    for obj in env.objects:
        if obj.type.name not in {"Texture2D", "Sprite"}:
            continue

        data = obj.read()
        name = get_obj_name(data)
        if name != args.target_name:
            continue

        if obj.type.name == "Texture2D":
            data.image = replacement_img
            data.save()
            replaced += 1
        else:
            # Sprite replacement is done via its texture. If sprite has direct image assignment in this UnityPy version, use it.
            if hasattr(data, "image"):
                data.image = replacement_img
                data.save()
                replaced += 1

    if replaced == 0:
        raise RuntimeError(f"No Texture2D/Sprite named '{args.target_name}' was replaced")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_environment(env, output_path)

    print(f"Replaced objects: {replaced}")
    print(f"Wrote modified bundle: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
