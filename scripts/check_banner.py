#!/usr/bin/env python3
"""TOMBO banner/tag integrity.

Asserts the version is consistent across: tombo.css banner (line 1),
tombo.js banner (line 1), and the vendoring pins (`git ... show vX.Y.Z:...`)
in README.md, index.html, and ja/index.html — three pins each. When run on a
tag (GITHUB_REF=refs/tags/vX.Y.Z), also asserts the tag matches. Exit 1 on
any mismatch.
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

def pin_versions(path: Path) -> list[str]:
    # lines like: git -C /path/to/tombo show v0.12.0:tombo.css > ...
    return [m.group(1) for m in re.finditer(r"show v(\d+\.\d+\.\d+):", path.read_text())]

def main() -> int:
    versions = {}
    versions["tombo.css banner"] = first_line_version(ROOT / "tombo.css")
    versions["tombo.js banner"] = first_line_version(ROOT / "tombo.js")

    pin_sources = [("README.md", 3), ("index.html", 3), ("ja/index.html", 3)]
    ok = True
    for name, want in pin_sources:
        got = pin_versions(ROOT / name)
        if len(got) != want:
            print(f"FAIL  expected {want} vendoring pins in {name}, found {len(got)}")
            ok = False
        for i, p in enumerate(got, 1):
            versions[f"{name} pin {i}"] = p
    if not ok:
        return 1

    print("versions found:")
    for k, v in versions.items():
        print(f"  {k:18} {v}")

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
    if ref.startswith("refs/tags/"):
        # any tag that triggered CI must be a strict vX.Y.Z release tag AND match
        m = re.fullmatch(r"refs/tags/v(\d+\.\d+\.\d+)", ref)
        if not m:
            print(f"FAIL  tag {ref.removeprefix('refs/tags/')} is not a vX.Y.Z release tag")
            return 1
        tag = m.group(1)
        if tag != agreed:
            print(f"FAIL  tag v{tag} != banner/pin v{agreed}")
            return 1
        print(f"PASS  tag v{tag} matches banners/pins")
    return 0

if __name__ == "__main__":
    sys.exit(main())
