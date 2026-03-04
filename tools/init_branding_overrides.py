#!/usr/bin/env python3
"""Initialize editable branding texture overrides from exported assets.

This keeps gameplay unchanged and gives a clean folder of PNGs you can edit.
"""

from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
ALL_ASSETS = ROOT / "extracted" / "all-assets"
OVERRIDES = ROOT / "extracted" / "branding-overrides"

TARGETS = {
    "slope_icon": ["Texture2D_slope_icon_33.png", "Sprite_slope_icon_92.png"],
    "loginBut": ["Texture2D_loginBut_5.png"],
    "registerBut": ["Texture2D_registerBut_9.png"],
    "UISprite": ["Texture2D_UISprite_19.png", "Sprite_UISprite_85.png"],
    "borderRed": ["Texture2D_borderRed_28.png", "Sprite_borderRed_89.png"],
    "borderRedThin": ["Texture2D_borderRedThin_22.png", "Sprite_borderRedThin_87.png"],
    "borderGreen": ["Texture2D_borderGreen_31.png", "Sprite_borderGreen_91.png"],
    "borderGreenThin": ["Texture2D_borderGreenThin_27.png", "Sprite_borderGreenThin_88.png"],
    "polygon": ["Texture2D_polygon_24.png"],
    "polygonThin": ["Texture2D_polygonThin_32.png"],
    "polygonRed": ["Texture2D_polygonRed_25.png"],
    "polygonRedThin": ["Texture2D_polygonRedThin_41.png"],
    "speedArrow": ["Texture2D_speedArrow_38.png"],
    "idnet_logo": ["Texture2D_idnet_logo_8.png"],
    "y8_new_logo": ["Texture2D_y8_new_logo_2.png", "Sprite_y8_new_logo_3.png"],
    "y8_new_logo_smaller": ["Texture2D_y8_new_logo_smaller_34.png", "Sprite_y8_new_logo_smaller_93.png"],
    "y8_new_logo_smaller_offset": ["Texture2D_y8_new_logo_smaller_offset_35.png"],
    "google-play-logo_small": ["Texture2D_google-play-logo_small_39.png", "Sprite_google-play-logo_small_95.png"],
    "Android-app-Amazafit": ["Texture2D_Android-app-Amazafit_42.png", "Sprite_Android-app-Amazafit_96.png"],
    "SoundOn": ["Texture2D_SoundOn_36.png", "Sprite_SoundOn_94.png"],
    "SoundOff": ["Texture2D_SoundOff_29.png", "Sprite_SoundOff_90.png"],
    "Background": ["Texture2D_Background_20.png", "Sprite_Background_86.png"],
    "ArrowLeft": ["Texture2D_ArrowLeft_4.png"],
    "ArrowRight": ["Texture2D_ArrowRight_6.png"],
    "textfield": ["Texture2D_textfield_10.png"],
    "grey": ["Texture2D_grey_3.png"],
    "white-bg": ["Texture2D_white-bg_12.png"],
    "loading": ["Texture2D_loading_11.png"],
    "close-x": ["Texture2D_close-x_7.png"],
}


def main() -> int:
    OVERRIDES.mkdir(parents=True, exist_ok=True)

    copied = 0
    missing = []

    for target_name, source_candidates in TARGETS.items():
        source = None
        for candidate in source_candidates:
            p = ALL_ASSETS / candidate
            if p.exists():
                source = p
                break

        if source is None:
            missing.append(target_name)
            continue

        dest = OVERRIDES / f"{target_name}.png"
        shutil.copy2(source, dest)
        copied += 1

    print(f"Copied override templates: {copied}")
    if missing:
        print("Missing templates for:")
        for m in missing:
            print(f"- {m}")
    print(f"Override folder: {OVERRIDES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
