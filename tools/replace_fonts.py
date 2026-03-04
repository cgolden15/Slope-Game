"""
Replace arial/arialbd in Unity bundle with Orbitron variable font.
Also updates m_FontNames so Unity doesn't fall back to system Arial.
Usage: python3 tools/replace_fonts.py
"""
import UnityPy
import os, sys

BUNDLE = "extracted/data/data.unity3d"
OUT    = "extracted/data/data.modified.unity3d"
# Orbitron variable font covers all weights in one file
ORBITRON = "/tmp/Orbitron-VF.ttf"
FONT_MAP = {
    "arial":                "arial",
    "arialbd":              "arialbd",
    "telegrama_render":     "telegrama_render",
    "telegrama_raw":        "telegrama_raw",
    "telegrama_raw_osn":    "telegrama_raw_osn",
    "telegrama_render_osn": "telegrama_render_osn",
    "6809char":             "6809CHAR",
}

env = UnityPy.load(BUNDLE)
replaced = []

for obj in env.objects:
    if obj.type.name != "Font":
        continue
    data = obj.read()
    name = getattr(data, "m_Name", None) or ""
    key = name.lower()
    if key not in FONT_MAP:
        continue

    with open(ORBITRON, "rb") as f:
        new_bytes = list(f.read())

    old_size = len(data.m_FontData) if data.m_FontData else 0
    data.m_FontData = new_bytes
    data.m_FontNames = ["Orbitron"]
    data.save()
    replaced.append((name, old_size, len(new_bytes)))
    print("Replaced: %s  old=%d new=%d bytes" % (name, old_size, len(new_bytes)))

if not replaced:
    print("No fonts replaced — check font names in bundle")
    sys.exit(1)

with open(OUT, "wb") as f:
    f.write(env.file.save())

print("Saved: %s" % OUT)
