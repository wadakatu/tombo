#!/usr/bin/env python3
"""TOMBO contrast gate — WCAG 2.1 relative luminance check.

Pairs and floors come from docs/superpowers/specs/2026-07-20-*.md §5.
Exit 1 if any pair is below its floor.
"""
import sys

def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

# (name, fg, bg, floor)
PAIRS = [
    ("light ink/paper",        "#1A211D", "#F2F4EF", 7.0),
    ("light ink-sub/paper",    "#4C5650", "#F2F4EF", 4.5),
    ("light green/paper",      "#0E5A47", "#F2F4EF", 4.5),
    ("light shu line/paper",   "#D8442B", "#F2F4EF", 3.0),
    ("light on-green/green",   "#F2F4EF", "#0E5A47", 4.5),
    ("light error text/paper", "#A6301C", "#F2F4EF", 4.5),
    ("light success dot/paper","#2C7A4B", "#F2F4EF", 3.0),
    ("light warn dot/paper",   "#B07818", "#F2F4EF", 3.0),
    ("dark ink/paper",         "#E5EBE6", "#131714", 7.0),
    ("dark ink-sub/paper",     "#9AA69F", "#131714", 4.5),
    ("dark green/paper",       "#4FC2A2", "#131714", 4.5),
    ("dark shu label/paper",   "#E5654C", "#131714", 4.5),
    ("dark on-green/green",    "#10201A", "#4FC2A2", 4.5),
    ("dark error text/paper",  "#D06A5A", "#131714", 4.5),
    ("dark success dot/paper", "#57B98A", "#131714", 3.0),
    ("dark warn dot/paper",    "#D9A441", "#131714", 3.0),
]

def self_test() -> None:
    assert abs(ratio("#FFFFFF", "#000000") - 21.0) < 0.01
    assert abs(ratio("#1A211D", "#F2F4EF") - 14.82) < 0.05
    assert abs(ratio("#4FC2A2", "#131714") - 8.25) < 0.05
    print("self-test OK")

def main() -> int:
    failed = False
    for name, fg, bg, floor in PAIRS:
        r = ratio(fg, bg)
        ok = r >= floor
        failed |= not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:26} {r:6.2f}  (floor {floor})")
    return 1 if failed else 0

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
        sys.exit(0)
    sys.exit(main())
