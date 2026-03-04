#!/usr/bin/env python3
"""Sync visible branding fields from name.md into web shell and build metadata."""

from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
NAME_FILE = ROOT / "name.md"
INDEX_FILE = ROOT / "index.html"
PROGRESS_FILE = ROOT / "TemplateData" / "UnityProgress.js"
SLOPE_JSON_FILE = ROOT / "Build" / "slope.json"


def read_brand_name() -> str:
    raw = NAME_FILE.read_text(encoding="utf-8").strip()
    if not raw:
        raise RuntimeError("name.md is empty")
    return raw.splitlines()[0].strip()


def patch_index_html(text: str, brand: str) -> str:
    text = re.sub(r"<title>.*?</title>", f"<title>{brand}</title>", text, count=1, flags=re.S)
    text = re.sub(r"<h1 class=\"brand\">.*?</h1>", f"<h1 class=\"brand\">{brand}</h1>", text, count=1, flags=re.S)
    return text


def patch_progress_js(text: str, brand: str) -> str:
    text = re.sub(r'title\.textContent\s*=\s*".*?";', f'title.textContent = "{brand}";', text, count=1)
    return text


def patch_slope_json(text: str, brand: str) -> str:
    data = json.loads(text)
    data["productName"] = brand
    if not data.get("companyName"):
        data["companyName"] = "Custom Brand"
    return json.dumps(data, ensure_ascii=False, indent=0)


def main() -> int:
    brand = read_brand_name()

    INDEX_FILE.write_text(patch_index_html(INDEX_FILE.read_text(encoding="utf-8"), brand), encoding="utf-8")
    PROGRESS_FILE.write_text(patch_progress_js(PROGRESS_FILE.read_text(encoding="utf-8"), brand), encoding="utf-8")
    SLOPE_JSON_FILE.write_text(patch_slope_json(SLOPE_JSON_FILE.read_text(encoding="utf-8"), brand), encoding="utf-8")

    print(f"Synced branding to: {brand}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
