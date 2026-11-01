#!/usr/bin/env python3
"""Generate agent entry points from current documentation; --check never writes."""
import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://raw.githubusercontent.com/wadakatu/tombo/main/"
SOURCES = [
    ("docs/ai.md", "Agent guide", "Integration workflow, constraints and verification"),
    ("docs/upgrading.md", "Upgrading", "Unreleased behavior changes, consumer verification and rollback"),
    ("docs/recipes.md", "Integration recipes", "Complete settings form and scrollable table compositions"),
    ("README.md", "Getting started", "Vendoring, license and repository checks"),
    ("docs/foundations.md", "Foundations", "Colors, typography and themes"),
    ("docs/layout.md", "Layout", "Containers, spacing and overflow"),
    ("docs/signatures.md", "Signatures", "Brand marks and visual intensity"),
    ("docs/forms.md", "Forms", "Native controls and accessible validation"),
    ("docs/topbar.md", "Topbar", "Application header and navigation"),
    ("docs/charts.md", "Charts", "Figures and accessible data alternatives"),
    ("docs/tombo-js.md", "Behavior", "Optional theme and copy behavior"),
    ("docs/print.md", "Print", "Print styles and trim marks"),
]


def resolve_link(path, destination):
    """Validate local file targets before making them absolute for consumers."""
    parsed = urlsplit(destination)
    if not parsed.scheme and not parsed.netloc and parsed.path:
        base = ROOT if parsed.path.startswith("/") else (ROOT / path).parent
        target = (base / unquote(parsed.path).lstrip("/")).resolve()
        if not target.is_relative_to(ROOT.resolve()):
            raise ValueError(f"Link escapes repository in {path}: {destination}")
        if not target.exists():
            raise ValueError(f"Missing link target in {path}: {destination}")
        if parsed.path.startswith("/"):
            # A local root is the repository, not raw.githubusercontent.com's root.
            return urljoin(BASE, destination.lstrip("/"))
    return urljoin(BASE + path, destination)


def render():
    index = ["# TOMBO", "", "> A single-file, zero-dependency CSS design system with optional JavaScript.", "",
             "This is main-branch documentation and may include unreleased changes.",
             "For an existing app, use its pinned release, not an automatic upgrade.", "",
             "## Reference", ""]
    full = ["# TOMBO — full reference", "", "Generated from current repository Markdown. Do not edit directly.",
            "Main-branch reference; match an existing application's pinned release before use.", ""]
    for path, title, description in SOURCES:
        source = ROOT / path
        if not source.is_file():
            raise ValueError(f"Missing indexed source: {path}")
        text = source.read_text(encoding="utf-8")
        index.append(f"- [{title}]({BASE}{path}): {description}.")
        # Rewrite ordinary Markdown link destinations, leaving code samples intact.
        parts = re.split(r"(```[\s\S]*?```)", text)
        for i in range(0, len(parts), 2):
            parts[i] = re.sub(r"(?<=\]\()([^\s)]+)(?=\))",
                              lambda m: resolve_link(path, m[1]), parts[i])
        full.extend([f"<!-- Source: {BASE}{path} -->", "", "".join(parts).rstrip(), "", "---", ""])
    index.extend(["", "## Optional", "",
                  f"- [Full reference]({BASE}llms-full.txt): Combined reference when link traversal is unavailable.",
                  f"- [Component catalog]({BASE}examples/components.html): Live HTML examples and copyable markup.",
                  f"- [CSS source]({BASE}tombo.css): Authoritative tokens and selectors.", ""])
    return {"llms.txt": "\n".join(index), "llms-full.txt": "\n".join(full)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    try:
        outputs = render()
    except ValueError as error:
        parser.exit(1, f"Agent docs: {error}\n")
    for name, content in outputs.items():
        target = ROOT / name
        if args.check:
            if not target.is_file() or target.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            target.write_text(content, encoding="utf-8")
    if stale:
        parser.exit(1, f"Stale agent docs: {', '.join(stale)}; run python3 scripts/build_agent_docs.py\n")
    print("Agent docs: current" if args.check else "Agent docs: generated")


if __name__ == "__main__":
    main()
