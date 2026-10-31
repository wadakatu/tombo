#!/usr/bin/env bash
# TOMBO gate — the five checks CI and local dev both run. Any failure aborts.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "── stylelint (use-baseline widely) ──";  npx --no-install stylelint tombo.css
echo "── contrast ──";                          python3 scripts/check_contrast.py --self-test; python3 scripts/check_contrast.py
echo "── size budget ──";                       python3 scripts/check_size.py
echo "── banner / tag ──";                      python3 scripts/check_banner.py
echo "── js syntax ──";                         node --check tombo.js
node scripts/check_theme.mjs
python3 scripts/check_agent_docs.py
python3 scripts/build_agent_docs.py --check
echo "✓ all gates passed"
