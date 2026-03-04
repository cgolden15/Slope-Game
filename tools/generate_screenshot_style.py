#!/usr/bin/env python3
"""
Generate all in-game UI textures matching the screenshot style:
- Dark mesh/grid background panels
- Neon green glowing rounded buttons
- Transparent ads
- Matching arrows, borders, spinners, sound icons, close-X
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "extracted" / "all-assets"
OUT  = ROOT / "extracted" / "branding-overrides"

# ── exact palette from screenshot ──────────────────────────────────────────
BLACK       = (0,   0,   0,  255)
NEAR_BLACK  = (10,  12,  10, 255)
DARK_PANEL  = (14,  18,  12, 255)    # panel bg
GRID_LINE   = (0,   60,  0,  140)    # faint green grid lines
NEON_CORE   = (101, 255,  0, 255)    # #65ff00 bright neon
NEON_DIM    = (50,  160,  0, 255)    # #32a000 darker neon
NEON_MID    = (62,  200,  0, 255)    # mid neon
BTN_TOP     = (60,  180,  0, 255)    # button gradient top
BTN_BOT     = (20,  90,   0, 255)    # button gradient bottom
BTN_BORDER  = (101, 255,  0, 255)    # bright neon border
BTN_SHINE   = (160, 255,  80, 180)   # inner top shine
TRANSP      = (0,   0,   0,   0)
WHITE       = (255, 255, 255, 255)

def orig_size(name: str) -> tuple[int, int]:
    for f in ORIG.iterdir():
        stem = f.stem  # e.g. "Texture2D_loginBut_5"
        # strip leading "Texture2D_" or "Sprite_"
        for prefix in ("Texture2D_", "Sprite_"):
            if stem.startswith(prefix):
                stem = stem[len(prefix):]
        # strip trailing _<number>
        parts = stem.rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit():
            stem = parts[0]
        if stem == name and f.suffix == ".png":
            return Image.open(f).size
    return (32, 32)

# ── drawing helpers ─────────────────────────────────────────────────────────

def vgradient(size, top, bot) -> Image.Image:
    w, h = size
    img = Image.new("RGBA", size)
    px  = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y]  # touch
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(4))
        for x in range(w):
            px[x, y] = c
    return img

def grid_bg(size: tuple[int, int]) -> Image.Image:
    """Dark panel with faint neon-green grid lines — matches game background."""
    w, h = size
    img  = Image.new("RGBA", size, NEAR_BLACK)
    draw = ImageDraw.Draw(img)
    step = max(4, min(w, h) // 8)
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=GRID_LINE, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=GRID_LINE, width=1)
    return img

def neon_button(size: tuple[int, int]) -> Image.Image:
    """Glowing rounded rectangle button — matches PLAY/LOGIN/SETTINGS buttons."""
    w, h = size
    if w < 4 or h < 4:
        # 2×2 solid — used as fill tint, just return neon colour
        return Image.new("RGBA", size, BTN_TOP)

    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    r    = max(3, int(min(w, h) * 0.30))

    # gradient fill
    fill = vgradient(size, BTN_TOP, BTN_BOT)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w-1, h-1), radius=r, fill=255)
    img.paste(fill, (0, 0), mask)

    # outer neon border (2px)
    bw = max(1, h // 14)
    draw.rounded_rectangle((0, 0, w-1, h-1), radius=r, outline=BTN_BORDER, width=bw)

    # inner top shine strip
    shine_h = max(2, h // 5)
    shine   = Image.new("RGBA", (w, shine_h), TRANSP)
    sdraw   = ImageDraw.Draw(shine)
    sdraw.rounded_rectangle((bw, bw, w-bw-1, shine_h + r), radius=r, fill=BTN_SHINE)
    # fade shine with gradient mask
    sm = Image.new("L", (w, shine_h), 0)
    spx = sm.load()
    for y in range(shine_h):
        a = int(180 * (1 - y / shine_h))
        for x in range(w):
            spx[x, y] = a
    img.paste(shine, (0, 0), sm)

    return img

def neon_border_tile(size: tuple[int, int], color=BTN_BORDER) -> Image.Image:
    """32×32 9-slice border tile with neon glow edge — for borderGreen variants."""
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    bw   = max(1, min(w, h) // 6)
    draw.rounded_rectangle((0, 0, w-1, h-1), radius=bw*2,
                            outline=color, width=bw, fill=TRANSP)
    return img

def neon_border_thin(size: tuple[int, int], color=NEON_MID) -> Image.Image:
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, w-1, h-1), radius=2,
                            outline=color, width=1, fill=TRANSP)
    return img

def red_border_tile(size: tuple[int, int]) -> Image.Image:
    RED = (200, 30, 0, 255)
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    bw   = max(1, min(w, h) // 6)
    draw.rounded_rectangle((0, 0, w-1, h-1), radius=bw*2,
                            outline=RED, width=bw, fill=TRANSP)
    return img

def red_border_thin(size: tuple[int, int]) -> Image.Image:
    RED = (180, 20, 0, 255)
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, w-1, h-1), radius=2,
                            outline=RED, width=1, fill=TRANSP)
    return img

def neon_arrow(size: tuple[int, int], direction: str) -> Image.Image:
    """Small neon arrow (ArrowLeft / ArrowRight / speedArrow)."""
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    mx, my = w // 2, h // 2
    if direction == "left":
        pts = [(w-1, 1), (1, my), (w-1, h-2)]
    elif direction == "right":
        pts = [(0, 1), (w-2, my), (0, h-2)]
    else:  # speed up arrow
        pts = [(mx, 0), (w-1, h-1), (0, h-1)]
    draw.polygon(pts, fill=NEON_CORE, outline=NEON_CORE)
    return img

def neon_close_x(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    pad = max(1, min(w, h) // 5)
    lw  = max(1, min(w, h) // 5)
    draw.line([(pad, pad), (w-pad-1, h-pad-1)], fill=NEON_CORE, width=lw)
    draw.line([(w-pad-1, pad), (pad, h-pad-1)], fill=NEON_CORE, width=lw)
    return img

def neon_sound(size: tuple[int, int], on: bool) -> Image.Image:
    """Speaker icon with neon glow arcs."""
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    col  = NEON_CORE
    # speaker body (left 40%)
    bx1, bx2 = int(w * 0.10), int(w * 0.40)
    by1, by2 = int(h * 0.30), int(h * 0.70)
    draw.rectangle([(bx1, by1), (bx2, by2)], fill=col)
    # cone
    draw.polygon([(bx2, by1), (bx2, by2), (int(w*0.60), int(h*0.85)),
                  (int(w*0.60), int(h*0.15))], fill=col)
    if on:
        # two arcs
        m = max(1, w // 12)
        draw.arc((int(w*0.62), int(h*0.25), int(w*0.80), int(h*0.75)),
                 -60, 60, fill=col, width=m)
        draw.arc((int(w*0.72), int(h*0.12), int(w*0.95), int(h*0.88)),
                 -60, 60, fill=col, width=m)
    else:
        # X cross
        draw.line([(int(w*0.65), int(h*0.30)), (int(w*0.90), int(h*0.70))],
                  fill=(200, 30, 0, 255), width=max(1, w//10))
        draw.line([(int(w*0.90), int(h*0.30)), (int(w*0.65), int(h*0.70))],
                  fill=(200, 30, 0, 255), width=max(1, w//10))
    return img

def neon_spinner(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img  = Image.new("RGBA", size, TRANSP)
    draw = ImageDraw.Draw(img)
    m    = max(4, w // 8)
    box  = (m, m, w-m-1, h-m-1)
    draw.arc(box, 0, 360,  fill=(20, 60, 0, 100), width=max(2, w//10))
    draw.arc(box, -90, 200, fill=NEON_CORE,         width=max(2, w//10))
    draw.arc(box, 200, 270, fill=NEON_MID,           width=max(2, w//10))
    return img

def dark_panel(size: tuple[int, int]) -> Image.Image:
    """UISprite / Background — dark mesh panel for 9-slice."""
    return grid_bg(size)

def ui_sprite(size: tuple[int, int]) -> Image.Image:
    """UISprite is used as dialog/panel background."""
    w, h = size
    img  = grid_bg(size)
    draw = ImageDraw.Draw(img)
    r    = max(2, min(w, h) // 5)
    draw.rounded_rectangle((0, 0, w-1, h-1), radius=r,
                            outline=(0, 80, 0, 160), width=1)
    return img

def dark_textfield(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img  = Image.new("RGBA", size, (12, 16, 10, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w-1, h-1), outline=(40, 100, 20, 180), width=1)
    return img

# ── master dispatch ─────────────────────────────────────────────────────────
AD_NAMES = {
    "y8_new_logo", "y8_new_logo_smaller", "y8_new_logo_smaller_offset",
    "google-play-logo_small", "Android-app-Amazafit", "idnet_logo",
}

def make(name: str) -> Image.Image:
    size = orig_size(name)
    if name in AD_NAMES:
        return Image.new("RGBA", size, TRANSP)
    dispatch = {
        "Background":              lambda s: dark_panel(s),
        "UISprite":                lambda s: ui_sprite(s),
        "loginBut":                lambda s: neon_button(s),
        "registerBut":             lambda s: neon_button(s),
        "grey":                    lambda s: Image.new("RGBA", s, (16, 20, 12, 255)),
        "white-bg":                lambda s: Image.new("RGBA", s, WHITE),
        "textfield":               lambda s: dark_textfield(s),
        "loading":                 lambda s: neon_spinner(s),
        "borderGreen":             lambda s: neon_border_tile(s),
        "borderGreenThin":         lambda s: neon_border_thin(s),
        "polygon":                 lambda s: neon_border_tile(s),
        "polygonThin":             lambda s: neon_border_thin(s),
        "borderRed":               lambda s: red_border_tile(s),
        "borderRedThin":           lambda s: red_border_thin(s),
        "polygonRed":              lambda s: red_border_tile(s),
        "polygonRedThin":          lambda s: red_border_thin(s),
        "ArrowLeft":               lambda s: neon_arrow(s, "left"),
        "ArrowRight":              lambda s: neon_arrow(s, "right"),
        "speedArrow":              lambda s: neon_arrow(s, "speed"),
        "close-x":                 lambda s: neon_close_x(s),
        "SoundOn":                 lambda s: neon_sound(s, True),
        "SoundOff":                lambda s: neon_sound(s, False),
    }
    fn = dispatch.get(name)
    if fn:
        return fn(size)
    # fallback: keep original
    for f in ORIG.iterdir():
        stem = f.stem
        for prefix in ("Texture2D_", "Sprite_"):
            if stem.startswith(prefix):
                stem = stem[len(prefix):]
        parts = stem.rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit():
            stem = parts[0]
        if stem == name:
            return Image.open(f).convert("RGBA")
    return Image.new("RGBA", size, TRANSP)

# ── run ─────────────────────────────────────────────────────────────────────
import json
CONFIG = ROOT / "branding" / "texture_overrides.json"
data   = json.loads(CONFIG.read_text())
overrides = data.get("overrides", [])

done = 0
for entry in overrides:
    name = entry["target"]
    img  = make(name)
    dest = ROOT / entry["png"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)
    print("Generated: %-40s %s" % (name, img.size))
    done += 1

print("\nTotal: %d textures generated" % done)
