#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.conf, a SilentSDDM preset, from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep scripts/__pycache__ out of the repo
ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
# Preset per variant: (template, background in backgrounds/, overrides). The dark
# template is Dragon's layout: a large clock top right and the form on the right of the
# crest wallpaper, which leaves that side black, so the art stays sharp under light text.
# Lotus centers the form. Overrides are {section: {key: value}}, with @role@ markers as
# in the templates. Wave's print is paler: it is darkened and blurred under the form, the
# clock and date are dark on the sky, the message is orange so it stands out from the
# blue water, and the toolbar, over the water, keeps light text.
WAVE_TOOLBAR = {"content-color": '"@ui.fg@"'}
SDDM = {
    "wave": ("dark", "kanagawa-wave-great-wave-dim", {
        "LockScreen": {"brightness": "-0.15"},
        "LockScreen.Clock": {"color": '"@ui.bg_m1@"'},
        "LockScreen.Date": {"color": '"@ui.bg_m1@"'},
        "LockScreen.Message": {"position": '"bottom-center"', "align": '"center"', "color": '"@diag.warning@"'},
        "LoginScreen": {"blur": "24", "brightness": "-0.25"},
        **{f"LoginScreen.MenuArea.{m}": WAVE_TOOLBAR for m in ("Session", "Layout", "Keyboard", "Power")},
    }),
    "dragon": ("dark", "kanagawa-dragon-great-wave-crest", {}),
    "lotus": ("light", "hokusai-great-wave-restored", {}),
}


def override(text, sections):
    """Set `key = value` in each [section] of an INI text; every override must hit a key."""
    out, section, left = [], None, {(sec, key) for sec, keys in sections.items() for key in keys}
    for line in text.splitlines(keepends=True):
        if line.startswith("["):
            section = line.strip()[1:-1]
        key = line.split("=")[0].strip()
        if "=" in line and key in sections.get(section, {}):
            line = f"{key} = {sections[section][key]}\n"
            left.discard((section, key))
        out.append(line)
    if left:
        sys.exit(f"SDDM overrides match no key: {sorted(left)}")
    return "".join(out)



def roles(variant):
    """Map each role to "#rrggbb"; a role missing from the palette raises KeyError later."""
    return {
        role: "#" + "".join(f"{c:02x}" for c in color["rgb"])
        for color in variant["colors"].values()
        for role in color["usage"]
    }


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        hexes = roles(variants[v])
        template, background, overrides = SDDM[v]
        extra = {"variant": v, "Variant": v.capitalize(), "background": background}
        text = override((ROOT / "scripts" / f"sddm-{template}.conf.in").read_text(), overrides)
        text = re.sub(r"@([A-Za-z_.0-9]+)@", lambda m: extra.get(m[1]) or hexes[m[1]], text)
        (ROOT / "themes" / f"kanagawa-{v}.conf").write_text(text)


if __name__ == "__main__":
    main()
