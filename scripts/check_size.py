#!/usr/bin/env python3
"""TOMBO size budget — gzipped-byte ceilings for the distributed files.

Catches silent bloat. Ceilings have headroom over the current sizes but fail
on a real regression (e.g. a near-doubling). Exit 1 if any file is over budget.
"""
import gzip
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (path, gzipped-byte ceiling)
BUDGET = [
    ("tombo.css", 12 * 1024),  # 12 KiB — current ~10.0 KiB
    ("tombo.js",   2 * 1024),  #  2 KiB — current ~1.2 KiB
]

def gz_size(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), 9))

def main() -> int:
    failed = False
    for name, ceiling in BUDGET:
        size = gz_size(ROOT / name)
        ok = size <= ceiling
        failed |= not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:10} {size:6} B gzip  (ceiling {ceiling} B)")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
