#!/usr/bin/env python3
"""Decompress Unity .unityweb files (gzip or brotli) into a local output folder.

Usage:
  /usr/bin/python3 tools/decompress_unityweb.py --build-dir Build --out-dir extracted/raw
"""

from __future__ import annotations

import argparse
import gzip
from pathlib import Path


GZIP_MAGIC = b"\x1f\x8b"


def _read_bytes(path: Path) -> bytes:
    with path.open("rb") as f:
        return f.read()


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)


def _try_brotli_decompress(data: bytes) -> bytes:
    try:
        import brotli  # type: ignore
    except Exception as exc:
        raise RuntimeError("brotli module not installed") from exc
    return brotli.decompress(data)


def decompress_unityweb(src: Path, dst: Path) -> str:
    data = _read_bytes(src)

    if data.startswith(GZIP_MAGIC):
        decompressed = gzip.decompress(data)
        _write_bytes(dst, decompressed)
        return "gzip"

    # Not gzip: try brotli
    try:
        decompressed = _try_brotli_decompress(data)
        _write_bytes(dst, decompressed)
        return "brotli"
    except Exception:
        # Fallback: copy as-is (identity)
        _write_bytes(dst, data)
        return "identity"


def infer_output_name(src_name: str) -> str:
    # Keep stem and use better extension for known artifacts
    stem = src_name.removesuffix(".unityweb")
    if "wasmcode" in stem:
        return f"{stem}.wasm"
    if "framework" in stem or "wasmframework" in stem:
        return f"{stem}.js"
    if "data" in stem:
        return f"{stem}.bin"
    if "memory" in stem:
        return f"{stem}.mem"
    return f"{stem}.bin"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-dir", default="Build")
    parser.add_argument("--out-dir", default="extracted/raw")
    args = parser.parse_args()

    build_dir = Path(args.build_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    unityweb_files = sorted(build_dir.glob("*.unityweb"))
    if not unityweb_files:
        raise SystemExit(f"No .unityweb files found in {build_dir}")

    print(f"Found {len(unityweb_files)} .unityweb files")
    for src in unityweb_files:
        dst = out_dir / infer_output_name(src.name)
        mode = decompress_unityweb(src, dst)
        print(f"[{mode:8}] {src.name} -> {dst}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
