#!/usr/bin/env python3
"""Rebuild a UnityWebData1.0 archive using original entry order with optional overrides.

Usage:
  /usr/bin/python3 tools/rebuild_unitywebdata.py \
    --original extracted/raw/slope_data.bin \
    --overlay-dir extracted/data \
    --output Build/slope_data.unityweb
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


MAGIC = b"UnityWebData1.0\x00"


def read_u32(blob: bytes, at: int) -> tuple[int, int]:
    return struct.unpack_from("<I", blob, at)[0], at + 4


def parse_entries(blob: bytes) -> list[tuple[str, int, int]]:
    if not blob.startswith(MAGIC):
        raise RuntimeError("Input is not UnityWebData1.0")

    cur = len(MAGIC)
    toc_end, cur = read_u32(blob, cur)

    entries: list[tuple[str, int, int]] = []
    while cur < toc_end:
        data_offset, cur = read_u32(blob, cur)
        size, cur = read_u32(blob, cur)
        name_len, cur = read_u32(blob, cur)
        name = blob[cur : cur + name_len].decode("utf-8", errors="replace")
        cur += name_len
        entries.append((name, data_offset, size))

    return entries


def build_archive(original_blob: bytes, overlay_dir: Path, output_path: Path) -> None:
    entries = parse_entries(original_blob)

    entry_payloads: list[tuple[str, bytes]] = []
    for name, data_offset, size in entries:
        overlay_path = overlay_dir / Path(name)
        if overlay_path.exists() and overlay_path.is_file():
            data = overlay_path.read_bytes()
        else:
            data = original_blob[data_offset : data_offset + size]
        entry_payloads.append((name, data))

    # First compute TOC size
    toc_size = sum(4 + 4 + 4 + len(name.encode("utf-8")) for name, _ in entry_payloads)
    toc_end = len(MAGIC) + 4 + toc_size

    # Build header+TOC
    out = bytearray()
    out.extend(MAGIC)
    out.extend(struct.pack("<I", toc_end))

    # Compute data offsets after TOC
    running_offset = toc_end
    toc_rows: list[bytes] = []
    for name, data in entry_payloads:
        name_bytes = name.encode("utf-8")
        toc_rows.append(
            struct.pack("<I", running_offset)
            + struct.pack("<I", len(data))
            + struct.pack("<I", len(name_bytes))
            + name_bytes
        )
        running_offset += len(data)

    for row in toc_rows:
        out.extend(row)

    # Append data
    for _, data in entry_payloads:
        out.extend(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(bytes(out))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", required=True)
    parser.add_argument("--overlay-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    original_blob = Path(args.original).read_bytes()
    build_archive(original_blob, Path(args.overlay_dir), Path(args.output))
    print(f"Wrote rebuilt archive to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
