#!/usr/bin/env python3
"""Extract a UnityWebData1.0 archive into files.

Usage:
  /usr/bin/python3 tools/extract_unitywebdata.py \
    --input extracted/raw/slope_data.bin \
    --out-dir extracted/data
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


MAGIC = b"UnityWebData1.0\x00"


def read_u32_le(data: bytes, offset: int) -> tuple[int, int]:
    return struct.unpack_from("<I", data, offset)[0], offset + 4


def sanitize_relative_path(name: str) -> Path:
    p = Path(name)
    if p.is_absolute():
        p = Path(*p.parts[1:])
    safe_parts = [part for part in p.parts if part not in ("..", "")]
    return Path(*safe_parts) if safe_parts else Path("unnamed.bin")


def extract_archive(input_path: Path, out_dir: Path) -> None:
    blob = input_path.read_bytes()

    if not blob.startswith(MAGIC):
        raise RuntimeError(
            f"{input_path} is not UnityWebData1.0 (missing magic header)."
        )

    cursor = len(MAGIC)
    toc_end, cursor = read_u32_le(blob, cursor)

    entries: list[tuple[int, int, str]] = []
    while cursor < toc_end:
        data_offset, cursor = read_u32_le(blob, cursor)
        size, cursor = read_u32_le(blob, cursor)
        name_len, cursor = read_u32_le(blob, cursor)
        name_bytes = blob[cursor : cursor + name_len]
        cursor += name_len
        name = name_bytes.decode("utf-8", errors="replace")
        entries.append((data_offset, size, name))

    print(f"TOC entries: {len(entries)}")

    out_dir.mkdir(parents=True, exist_ok=True)

    for index, (data_offset, size, name) in enumerate(entries, start=1):
        rel_path = sanitize_relative_path(name)
        dst = out_dir / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        data = blob[data_offset : data_offset + size]
        dst.write_bytes(data)
        print(f"[{index:04d}/{len(entries):04d}] {rel_path} ({size} bytes)")



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="extracted/data")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    extract_archive(input_path, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
