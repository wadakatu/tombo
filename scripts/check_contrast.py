#!/usr/bin/env python3
"""TOMBO contrast gate — WCAG 2.1 relative luminance check.

Token values are parsed from tombo.css (the single source of truth), so a
token edit there is checked automatically. Pairs and floors come from
docs/superpowers/specs/2026-07-20-*.md §5.
Exit 1 if any pair is below its floor or references a missing token.
"""
import re
import sys
from pathlib import Path

CSS_PATH = Path(__file__).resolve().parent.parent / "tombo.css"

TOKEN_RE = re.compile(
    r"--tombo-([a-z-]+):\s*light-dark\(\s*(#[0-9A-Fa-f]{6})\s*,\s*(#[0-9A-Fa-f]{6})\s*\)"
)

def load_tokens(css_path: Path = CSS_PATH) -> dict:
    """Parse every `--tombo-*: light-dark(#hex, #hex)` declaration."""
    tokens = {}
    for name, light, dark in TOKEN_RE.findall(css_path.read_text()):
        tokens[name] = {"light": light, "dark": dark}
    return tokens

def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

# (label, theme, fg token, bg token, floor)
PAIRS = [
    ("light ink/paper",           "light", "ink",           "paper",   7.0),
    ("light ink-sub/paper",       "light", "ink-sub",       "paper",   4.5),
    ("light ink-faint/paper",     "light", "ink-faint",     "paper",   4.5),
    ("light green/paper",         "light", "green",         "paper",   4.5),
    ("light shu line/paper",      "light", "shu",           "paper",   3.0),
    ("light on-green/green",      "light", "on-green",      "green",   4.5),
    ("light error text/paper",    "light", "error",         "paper",   4.5),
    ("light success dot/paper",   "light", "success",       "paper",   3.0),
    ("light warn dot/paper",      "light", "warn",          "paper",   3.0),
    ("light callout-label/paper", "light", "callout-label", "paper",   4.5),
    ("light ink/surface",         "light", "ink",           "surface", 7.0),
    ("light ink-sub/surface",     "light", "ink-sub",       "surface", 4.5),
    ("light ink-faint/surface",   "light", "ink-faint",     "surface", 4.5),
    ("dark ink/paper",            "dark",  "ink",           "paper",   7.0),
    ("dark ink-sub/paper",        "dark",  "ink-sub",       "paper",   4.5),
    ("dark ink-faint/paper",      "dark",  "ink-faint",     "paper",   4.5),
    ("dark green/paper",          "dark",  "green",         "paper",   4.5),
    ("dark shu label/paper",      "dark",  "shu",           "paper",   4.5),
    ("dark on-green/green",       "dark",  "on-green",      "green",   4.5),
    ("dark error text/paper",     "dark",  "error",         "paper",   4.5),
    ("dark success dot/paper",    "dark",  "success",       "paper",   3.0),
    ("dark warn dot/paper",       "dark",  "warn",          "paper",   3.0),
    ("dark callout-label/paper",  "dark",  "callout-label", "paper",   4.5),
    ("dark ink/surface",          "dark",  "ink",           "surface", 7.0),
    ("dark ink-sub/surface",      "dark",  "ink-sub",       "surface", 4.5),
    ("dark ink-faint/surface",    "dark",  "ink-faint",     "surface", 4.5),
]

def self_test() -> None:
    assert abs(ratio("#FFFFFF", "#000000") - 21.0) < 0.01
    assert abs(ratio("#1A211D", "#F2F4EF") - 14.82) < 0.05
    assert abs(ratio("#4FC2A2", "#131714") - 8.25) < 0.05
    tokens = load_tokens()
    assert tokens["ink"]["light"] == "#1A211D", "tombo.css parse drift"
    assert {"paper", "surface", "green", "shu"} <= tokens.keys()
    print("self-test OK")

def main() -> int:
    tokens = load_tokens()
    failed = False
    for label, theme, fg, bg, floor in PAIRS:
        if fg not in tokens or bg not in tokens:
            missing = fg if fg not in tokens else bg
            print(f"FAIL  {label:26}   n/a  (token --tombo-{missing} not found in tombo.css)")
            failed = True
            continue
        r = ratio(tokens[fg][theme], tokens[bg][theme])
        ok = r >= floor
        failed |= not ok
        print(f"{'PASS' if ok else 'FAIL'}  {label:26} {r:6.2f}  (floor {floor})")
    return 1 if failed else 0

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
        sys.exit(0)
    sys.exit(main())
