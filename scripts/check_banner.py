#!/usr/bin/env python3
"""TOMBO banner/tag integrity.

Asserts the version is consistent across: tombo.css banner (line 1),
tombo.js banner (line 1), and the three README vendoring pins
(`git ... show vX.Y.Z:...`). When run on a tag (GITHUB_REF=refs/tags/vX.Y.Z),
also asserts the tag matches. Exit 1 on any mismatch.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VER = re.compile(r"v(\d+\.\d+\.\d+)")

def first_line_version(path: Path) -> str | None:
    line = path.read_text().splitlines()[0]
    m = VER.search(line)
    return m.group(1) if m else None

def readme_pin_versions(path: Path) -> list[str]:
    # lines like: git -C /path/to/tombo show v0.12.0:tombo.css > ...
    return [m.group(1) for m in re.finditer(r"show v(\d+\.\d+\.\d+):", path.read_text())]

def main() -> int:
    versions = {}
    versions["tombo.css banner"] = first_line_version(ROOT / "tombo.css")
    versions["tombo.js banner"] = first_line_version(ROOT / "tombo.js")
    pins = readme_pin_versions(ROOT / "README.md")
    for i, p in enumerate(pins, 1):
        versions[f"README pin {i}"] = p

    print("versions found:")
    for k, v in versions.items():
        print(f"  {k:18} {v}")

    if len(pins) != 3:
        print(f"FAIL  expected 3 README vendoring pins, found {len(pins)}")
        return 1
    if None in versions.values():
        print("FAIL  a banner has no vX.Y.Z version")
        return 1
    found = list(versions.values())
    if len(set(found)) != 1:
        print(f"FAIL  version mismatch across banners/pins: {sorted(set(found))}")
        return 1
    agreed = found[0]
    print(f"PASS  all banners and pins agree: v{agreed}")

    ref = os.environ.get("GITHUB_REF", "")
    m = re.fullmatch(r"refs/tags/v(\d+\.\d+\.\d+)", ref)
    if m:
        tag = m.group(1)
        if tag != agreed:
            print(f"FAIL  tag v{tag} != banner/pin v{agreed}")
            return 1
        print(f"PASS  tag v{tag} matches banners/pins")
    return 0

if __name__ == "__main__":
    sys.exit(main())
