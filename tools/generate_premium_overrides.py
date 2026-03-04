#!/usr/bin/env python3
"""Generate premium-themed in-game UI textures from override templates.

This keeps dimensions identical and only changes visuals.
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
NAME_PATH = ROOT / "name.md"
OVERRIDE_DIR = ROOT / "extracted" / "branding-overrides"

GOLD_A = (213, 164, 78, 255)
GOLD_B = (243, 204, 122, 255)
DARK_A = (19, 16, 12, 255)
DARK_B = (38, 30, 19, 255)
OFF_WHITE = (253, 247, 234, 255)


def get_brand() -> str:
    raw = NAME_PATH.read_text(encoding="utf-8").strip()
    return raw.splitlines()[0].strip() if raw else "Slope™: Premium Edition"


def gradient(size: tuple[int, int], top: tuple[int, int, int, int], bottom: tuple[int, int, int, int]) -> Image.Image:
    w, h = size
    out = Image.new("RGBA", size)
    px = out.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        a = int(top[3] + (bottom[3] - top[3]) * t)
        for x in range(w):
            px[x, y] = (r, g, b, a)
    return out


def rounded_button(size: tuple[int, int], label: str) -> Image.Image:
    w, h = size
    if w < 4 or h < 4:
        return flat_plate(size, alpha=220)

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = max(4, int(min(w, h) * 0.24))
    fill = gradient(size, DARK_A, DARK_B)

    mask = Image.new("L", size, 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    img.paste(fill, (0, 0), mask)

    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, outline=GOLD_A, width=max(1, h // 14))
    if w > 3 and h > 3:
        draw.rounded_rectangle((1, 1, w - 2, h - 2), radius=max(1, radius - 1), outline=(243, 204, 122, 150), width=1)

    font = ImageFont.load_default()
    text = label.upper()
    tw, th = draw.textbbox((0, 0), text, font=font)[2:4]
    draw.text(((w - tw) / 2, (h - th) / 2 - 1), text, fill=OFF_WHITE, font=font)
    return img


def stripe_arrow(size: tuple[int, int], direction: str) -> Image.Image:
    w, h = size
    if w < 3 or h < 3:
        return flat_plate(size, alpha=220)

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=max(3, min(w, h) // 4), fill=(30, 24, 16, 220), outline=GOLD_A, width=1)

    if direction == "left":
        pts = [(int(w * 0.62), int(h * 0.2)), (int(w * 0.38), int(h * 0.5)), (int(w * 0.62), int(h * 0.8))]
    else:
        pts = [(int(w * 0.38), int(h * 0.2)), (int(w * 0.62), int(h * 0.5)), (int(w * 0.38), int(h * 0.8))]
    draw.polygon(pts, fill=GOLD_B)
    return img


def border_tile(size: tuple[int, int], thin: bool = False) -> Image.Image:
    w, h = size
    if w < 2 or h < 2:
        return flat_plate(size, alpha=220)

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    stroke = 1 if thin else max(1, min(w, h) // 8)
    draw.rectangle((0, 0, w - 1, h - 1), outline=GOLD_A, width=stroke)
    return img


def sound_icon(size: tuple[int, int], on: bool) -> Image.Image:
    w, h = size
    if w < 6 or h < 6:
        return flat_plate(size, alpha=220)

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.ellipse((1, 1, w - 2, h - 2), fill=(28, 22, 14, 240), outline=GOLD_A, width=max(1, w // 16))

    cx, cy = w // 2, h // 2
    spk = [(cx - w * 0.18, cy - h * 0.1), (cx - w * 0.05, cy - h * 0.1), (cx + w * 0.02, cy - h * 0.22), (cx + w * 0.02, cy + h * 0.22), (cx - w * 0.05, cy + h * 0.1), (cx - w * 0.18, cy + h * 0.1)]
    draw.polygon(spk, fill=OFF_WHITE)

    if on:
        draw.arc((cx, cy - h * 0.22, cx + w * 0.38, cy + h * 0.22), start=-45, end=45, fill=GOLD_B, width=max(1, w // 16))
        draw.arc((cx + w * 0.02, cy - h * 0.32, cx + w * 0.52, cy + h * 0.32), start=-45, end=45, fill=GOLD_A, width=max(1, w // 20))
    else:
        draw.line((cx + w * 0.08, cy - h * 0.2, cx + w * 0.32, cy + h * 0.2), fill=(210, 94, 82, 255), width=max(1, w // 14))
        draw.line((cx + w * 0.32, cy - h * 0.2, cx + w * 0.08, cy + h * 0.2), fill=(210, 94, 82, 255), width=max(1, w // 14))
    return img


def speed_arrow(size: tuple[int, int]) -> Image.Image:
    w, h = size
    if w < 4 or h < 4:
        return flat_plate(size, alpha=220)

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(0, h // 2), (int(w * 0.62), 0), (int(w * 0.62), int(h * 0.3)), (w, int(h * 0.3)), (w, int(h * 0.7)), (int(w * 0.62), int(h * 0.7)), (int(w * 0.62), h)], fill=GOLD_B)
    draw.line((0, h // 2, w, h // 2), fill=GOLD_A, width=max(1, h // 10))
    return img


def logo_plate(size: tuple[int, int], text: str) -> Image.Image:
    w, h = size
    if w < 3 or h < 3:
        return flat_plate(size, alpha=220)

    img = gradient(size, (24, 19, 12, 255), (38, 29, 18, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w - 1, h - 1), outline=GOLD_A, width=max(1, min(w, h) // 20))
    font = ImageFont.load_default()
    label = text[:16]
    tw, th = draw.textbbox((0, 0), label, font=font)[2:4]
    draw.text(((w - tw) / 2, (h - th) / 2), label, font=font, fill=OFF_WHITE)
    return img


def background(size: tuple[int, int]) -> Image.Image:
    return gradient(size, (20, 16, 12, 255), (44, 34, 22, 255))


def flat_plate(size: tuple[int, int], alpha: int = 210) -> Image.Image:
    return Image.new("RGBA", size, (31, 24, 15, alpha))


def make_texture(name: str, size: tuple[int, int], brand: str) -> Image.Image:
    if name == "loginBut":
        return rounded_button(size, "Login")
    if name == "registerBut":
        return rounded_button(size, "Register")
    if name == "ArrowLeft":
        return stripe_arrow(size, "left")
    if name == "ArrowRight":
        return stripe_arrow(size, "right")
    if name in {"SoundOn"}:
        return sound_icon(size, True)
    if name in {"SoundOff"}:
        return sound_icon(size, False)
    if name in {"borderRed", "borderGreen"}:
        return border_tile(size, thin=False)
    if name in {"borderRedThin", "borderGreenThin"}:
        return border_tile(size, thin=True)
    if name in {"speedArrow"}:
        return speed_arrow(size)
    if name in {"Background", "grey", "white-bg", "textfield", "loading", "UISprite"}:
        return background(size)
    if name in {"polygon", "polygonThin", "polygonRed", "polygonRedThin"}:
        return flat_plate(size, alpha=180)
    if name == "close-x":
        img = flat_plate(size, alpha=0)
        draw = ImageDraw.Draw(img)
        draw.line((0, 0, size[0] - 1, size[1] - 1), fill=GOLD_B, width=max(1, min(size) // 8))
        draw.line((size[0] - 1, 0, 0, size[1] - 1), fill=GOLD_B, width=max(1, min(size) // 8))
        return img
    if name == "slope_icon":
        return logo_plate(size, brand)
    if name in {"idnet_logo", "y8_new_logo", "y8_new_logo_smaller", "y8_new_logo_smaller_offset", "google-play-logo_small", "Android-app-Amazafit"}:
        return logo_plate(size, "Your Brand")
    return background(size)


def main() -> int:
    brand = get_brand()
    files = sorted(OVERRIDE_DIR.glob("*.png"))
    updated = 0

    for path in files:
        name = path.stem
        src = Image.open(path).convert("RGBA")
        out = make_texture(name, src.size, brand)
        out.save(path)
        updated += 1

    print(f"Generated premium overrides: {updated}")
    print(f"Brand used: {brand}")
    print(f"Folder: {OVERRIDE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
