"""
Revert branding-overrides/ back to original exported textures from all-assets/.
Run this to undo premium texture generation and restore originals.
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "branding" / "texture_overrides.json"
ALL_ASSETS = ROOT / "extracted" / "all-assets"
OVERRIDE_DIR = ROOT / "extracted" / "branding-overrides"

data = json.loads(CONFIG.read_text())
overrides = data.get("overrides", data) if isinstance(data, dict) else data
reverted = 0
missing = []

for entry in overrides:
    name = entry["target"]
    override_path = ROOT / entry["png"]

    # Find matching original in all-assets by texture name
    candidates = list(ALL_ASSETS.glob("Texture2D_%s_*.png" % name)) + \
                 list(ALL_ASSETS.glob("Sprite_%s_*.png" % name))
    if not candidates:
        missing.append(name)
        continue

    src = candidates[0]
    shutil.copy2(src, override_path)
    reverted += 1
    print("Reverted: %s -> %s" % (src.name, override_path.name))

print("\nReverted: %d  Missing originals: %d %s" % (reverted, len(missing), missing if missing else ""))
