#!/usr/bin/env python3
"""
Generates:
  1. Transparent PNGs for all ad/promo textures (y8, google-play, Amazafit, idnet)
  2. Dark-neon themed PNGs for UI panel textures matching the website palette
Writes directly into extracted/branding-overrides/
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw
import math

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "extracted" / "all-assets"
OUT  = ROOT / "extracted" / "branding-overrides"

# ── palette (mirrors style.css) ────────────────────────────────────────────
BG         = (9,   9,   9,  255)   # --bg
PANEL      = (14,  18,  12, 255)   # dark green-tinted panel
BORDER     = (101, 255,  0,  80)   # neon green border at low alpha
NEON_A     = (62,  166,  0, 255)   # --accent-a (login button fill)
NEON_B     = (101, 255,  0, 255)   # --accent-b (bright neon)
WHITE      = (255, 255, 255, 255)
TRANSP     = (0,   0,   0,   0)

def original_size(name: str) -> tuple[int, int]:
    for f in ORIG.iterdir():
        if f.name.startswith("Texture2D_" + name + "_") and f.suffix == ".png":
            return Image.open(f).size
    return (32, 32)

# ── helpers ────────────────────────────────────────────────────────────────
def transparent(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", size, TRANSP)

def solid(size: tuple[int, int], color: tuple[int, int, int, int]) -> Image.Image:
    return Image.new("RGBA", size, color)

def dark_panel_sprite(size: tuple[int, int]) -> Image.Image:
    """9-slice compatible rounded panel: dark fill + subtle neon border."""
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    r = max(2, min(6, w // 5, h // 5))
    # fill
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=PANEL)
    # border
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, outline=BORDER, width=1)
    return img

def neon_spinner(size: tuple[int, int]) -> Image.Image:
    """Circular neon-green spinner arc for loading texture."""
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    margin = max(4, w // 8)
    box = (margin, margin, w - margin - 1, h - margin - 1)
    # dim track
    draw.arc(box, 0, 360, fill=(40, 80, 20, 120), width=max(2, w // 10))
    # bright arc
    draw.arc(box, -90, 210, fill=NEON_B, width=max(2, w // 10))
    return img

def neon_button(size: tuple[int, int], color: tuple) -> Image.Image:
    """Solid 2x2 colour used as 9-slice button fill."""
    return Image.new("RGBA", size, color)

def dark_textfield(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img  = Image.new("RGBA", size, (16, 20, 14, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w - 1, h - 1), outline=(50, 100, 30, 200), width=1)
    return img

# ── texture map ────────────────────────────────────────────────────────────
# ad_names → transparent
AD_NAMES = [
    "y8_new_logo",
    "y8_new_logo_smaller",
    "y8_new_logo_smaller_offset",
    "google-play-logo_small",
    "Android-app-Amazafit",
    "idnet_logo",
]

def make_texture(name: str) -> Image.Image | None:
    size = original_size(name)
    # --- ads: go fully transparent
    if name in AD_NAMES:
        return transparent(size)
    # --- UI panel sprites
    if name in ("Background", "UISprite"):
        return dark_panel_sprite(size)
    # --- solid colour buttons (2x2)
    if name == "loginBut":
        return neon_button(size, NEON_A)
    if name == "registerBut":
        return neon_button(size, (30, 110, 0, 255))
    if name == "grey":
        return neon_button(size, (18, 22, 14, 255))
    if name == "white-bg":
        return neon_button(size, WHITE)
    # --- textfield
    if name == "textfield":
        return dark_textfield(size)
    # --- loading spinner
    if name == "loading":
        return neon_spinner(size)
    return None

# ── run ────────────────────────────────────────────────────────────────────
ALL_TARGETS = AD_NAMES + [
    "Background", "UISprite", "loginBut", "registerBut",
    "grey", "white-bg", "textfield", "loading",
]

done = 0
for name in ALL_TARGETS:
    img = make_texture(name)
    if img is None:
        print("SKIP (no generator):", name)
        continue
    dest = OUT / (name + ".png")
    img.save(dest)
    print("Generated:", name, img.size)
    done += 1

print("\nTotal generated:", done)
