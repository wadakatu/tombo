#!/usr/bin/env python3
"""TOMBO size budget — gzipped-byte ceilings for the distributed files.

Catches silent bloat and stale measurements in the introduction pages.
Exit 1 if a file is over budget or a page needs its measurements refreshed.
"""
import argparse
import gzip
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (path, gzipped-byte ceiling)
BUDGET = [
    ("tombo.css", 12 * 1024),  # 12 KiB
    ("tombo.js",   2 * 1024),  #  2 KiB
]
PAGES = ("index.html", "ja/index.html")

def gz_size(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), 9, mtime=0))


def page_values(sizes: dict[str, int]) -> dict[str, str]:
    ceilings = dict(BUDGET)
    css = sizes["tombo.css"]
    kb = f"{css / 1000:.1f}"  # Decimal KB, distinct from the KiB budget.
    percent = f"{css / ceilings['tombo.css'] * 100:.1f}"
    return {
        "css-label": f"MIT · CSS {kb} KB GZIP",
        "css-value": f"{kb}<small>KB</small>",
        "ruler": f'<div class="tombo-ruler" style="--tombo-ruler-value:{percent}%"></div>',
        "css-bytes": f"{css:,} B",
        "css-ceiling": f"{ceilings['tombo.css']:,} B",
        "js-bytes": f"{sizes['tombo.js']:,} B",
        "js-ceiling": f"{ceilings['tombo.js']:,} B",
    }


def render_page(source: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        start, end = f"<!-- size:{key} -->", f"<!-- /size:{key} -->"
        if source.count(start) != 1 or source.count(end) != 1:
            raise ValueError(f"expected exactly one size:{key} marker pair")
        pattern = re.escape(start) + r".*?" + re.escape(end)
        source, count = re.subn(pattern, lambda _: start + value + end, source, flags=re.S)
        if count != 1:
            raise ValueError(f"invalid size:{key} marker order")
    return source

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="refresh measured values in both introduction pages")
    args = parser.parse_args()
    failed = False
    sizes = {}
    for name, ceiling in BUDGET:
        size = gz_size(ROOT / name)
        sizes[name] = size
        ok = size <= ceiling
        failed |= not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:10} {size:6} B gzip  (ceiling {ceiling} B)")
    for name in PAGES:
        path = ROOT / name
        source = path.read_text(encoding="utf-8")
        try:
            expected = render_page(source, page_values(sizes))
        except ValueError as error:
            print(f"FAIL  {name}: {error}")
            failed = True
            continue
        if source == expected:
            print(f"PASS  {name}: measured sizes are current")
        elif args.write:
            path.write_text(expected, encoding="utf-8")
            print(f"WRITE {name}: refreshed measured sizes")
        else:
            print(f"FAIL  {name}: stale sizes; run python3 scripts/check_size.py --write")
            failed = True
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
