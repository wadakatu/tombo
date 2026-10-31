#!/usr/bin/env python3
"""TOMBO contrast gate — WCAG 2.1 relative luminance check.

Token values are parsed from tombo.css (the single source of truth), so a
token edit there is checked automatically. Pairs and floors come from
docs/superpowers/specs/2026-07-20-*.md §5.
Exit 1 if any pair is below its floor or references a missing token.
"""
import re
import sys
import tempfile
from pathlib import Path

CSS_PATH = Path(__file__).resolve().parent.parent / "tombo.css"

TOKEN_RE = re.compile(
    r"--tombo-([a-z-]+):\s*light-dark\(\s*(#[0-9A-Fa-f]{6})\s*,\s*(#[0-9A-Fa-f]{6})\s*\)"
)
PLAIN_RE = re.compile(r"--tombo-([a-z-]+):\s*(#[0-9A-Fa-f]{6})\s*;")

def load_tokens(css_path: Path = CSS_PATH) -> dict:
    """Parse `--tombo-*: light-dark(#hex, #hex)` and plain `--tombo-*: #hex` declarations."""
    text = css_path.read_text()
    tokens = {}
    for name, light, dark in TOKEN_RE.findall(text):
        tokens[name] = {"light": light, "dark": dark}
    for name, value in PLAIN_RE.findall(text):
        tokens[name] = {"light": value, "dark": value}
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
    ("light code-faint/code-bg",  "light", "code-faint",    "code-bg", 4.5),
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
    ("dark code-faint/code-bg",   "dark",  "code-faint",    "code-bg", 4.5),
]

# Supported text and focus combinations beyond the original paper/surface gate.
# Raised deliberately excludes faint/error: see docs/foundations.md.
for theme in ("light", "dark"):
    for bg in ("surface", "raised"):
        PAIRS.append((f"{theme} green/{bg}", theme, "green", bg, 4.5))
    for fg, floor in (("ink", 7.0), ("ink-sub", 4.5)):
        PAIRS.append((f"{theme} {fg}/raised", theme, fg, "raised", floor))
    PAIRS.append((f"{theme} error/surface", theme, "error", "surface", 4.5))

# Keyboard focus on the always-dark code panel (WCAG non-text contrast).
for theme in ("light", "dark"):
    PAIRS.append((f"{theme} code focus", theme, "code-green", "code-bg", 3.0))

# --- .tombo-glow ---------------------------------------------------------
# A lit surface is a COMPOSITE: the wash paints over paper/surface before any
# text lands on it, so a plain token-vs-token check cannot see it. v0.4 shipped
# a mock whose annotations measured 3.93:1 and 3.68:1 against exactly this and
# the gate stayed green. Read the overlay colors and alphas from the --tombo-glow-* tokens.
def load_glow(css_path: Path = CSS_PATH) -> dict:
    """Read supported transparent-day / rgba-night glow tokens; fail on drift."""
    text = css_path.read_text()
    result = {}
    for name in ("wash", "edge"):
        match = re.search(
            rf"--tombo-glow-{name}:\s*light-dark\(\s*transparent\s*,\s*rgba\("
            r"\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([0-9.]+)\s*\)\s*\)", text)
        if not match:
            raise ValueError(f"unsupported or missing --tombo-glow-{name}")
        r, g, b = map(int, match.groups()[:3])
        alpha = float(match[4])
        if max(r, g, b) > 255 or not 0 <= alpha <= 1:
            raise ValueError(f"invalid --tombo-glow-{name}")
        result[name] = (f"#{r:02X}{g:02X}{b:02X}", alpha)
    return result

# (label, fg token, bg token, overlay alpha, floor) — night only; the tokens are
# transparent by day, so the composite equals the plain background there.
GLOW_PAIRS = [
    ("glow hero ink",         "ink",                  "paper",   "wash", 7.0),
    ("glow hero annotation",  "ink-sub",              "paper",   "wash", 4.5),
    ("glow hero green",       "green",                "paper",   "wash", 4.5),
    ("glow hero shu line",    "shu",                  "paper",   "wash", 3.0),
    ("glow panel ink",        "ink",                  "surface", "edge", 7.0),
    ("glow panel annotation", "ink-sub",              "surface", "edge", 4.5),
    ("glow panel shu line",   "shu",                  "surface", "edge", 3.0),
    # the lift itself: inside .tombo-glow, --tombo-ink-faint becomes this token
    ("glow lifted faint",     "ink-faint-glow",       "paper",   "wash", 4.5),
]

def _hex_to_rgb(h: str) -> tuple:
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

def _rgb_to_hex(rgb) -> str:
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, round(c))) for c in rgb))

def composite(over_hex: str, alpha: float, under_hex: str) -> str:
    """Flatten `over` at `alpha` onto `under` — what the eye actually sees."""
    o, u = _hex_to_rgb(over_hex), _hex_to_rgb(under_hex)
    return _rgb_to_hex(tuple(uu * (1 - alpha) + oo * alpha for oo, uu in zip(o, u)))

def self_test() -> None:
    assert abs(ratio("#FFFFFF", "#000000") - 21.0) < 0.01
    assert abs(ratio("#1A211D", "#F2F4EF") - 14.82) < 0.05
    assert abs(ratio("#4FC2A2", "#131714") - 8.25) < 0.05
    tokens = load_tokens()
    assert tokens["ink"]["light"] == "#1A211D", "tombo.css parse drift"
    assert {"paper", "surface", "green", "shu"} <= tokens.keys()
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory) / "tokens.css"
        source = CSS_PATH.read_text()
        original = load_glow()
        fixture.write_text(source.replace("rgba(79,194,162,.16)", "rgba(255,255,255,.9)"))
        changed = load_glow(fixture)
        assert changed["wash"] == ("#FFFFFF", 0.9)
        assert changed["edge"] == original["edge"]
        lit = composite(*changed["wash"], tokens["paper"]["dark"])
        assert ratio(tokens["ink-sub"]["dark"], lit) < 4.5
        fixture.write_text(source.replace("--tombo-glow-wash:", "--removed-glow-wash:"))
        try:
            load_glow(fixture)
        except ValueError:
            pass
        else:
            raise AssertionError("missing overlay must fail closed")
    print("self-test OK")

def main() -> int:
    tokens = load_tokens()
    failed = False
    try:
        glow = load_glow()
    except ValueError as error:
        print(f"FAIL  {error}")
        return 1
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

    # the lift must actually equal ink-faint by day and ink-sub by night, or the
    # comment in tombo.css is a lie and one of the two themes silently shifts
    if "ink-faint-glow" in tokens:
        want = (tokens["ink-faint"]["light"], tokens["ink-sub"]["dark"])
        got = (tokens["ink-faint-glow"]["light"], tokens["ink-faint-glow"]["dark"])
        ok = want == got
        failed |= not ok
        print(f"{'PASS' if ok else 'FAIL'}  {'glow lift mirrors tokens':26}        "
              f"({got[0]}/{got[1]} vs {want[0]}/{want[1]})")

    for label, fg, bg, overlay, floor in GLOW_PAIRS:
        if fg not in tokens or bg not in tokens:
            missing = fg if fg not in tokens else bg
            print(f"FAIL  {label:26}   n/a  (token --tombo-{missing} not found)")
            failed = True
            continue
        color, alpha = glow[overlay]
        lit = composite(color, alpha, tokens[bg]["dark"])
        r = ratio(tokens[fg]["dark"], lit)
        ok = r >= floor
        failed |= not ok
        print(f"{'PASS' if ok else 'FAIL'}  {label:26} {r:6.2f}  (floor {floor}, on {lit})")

    return 1 if failed else 0

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
        sys.exit(0)
    sys.exit(main())
