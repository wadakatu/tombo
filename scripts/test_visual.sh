#!/usr/bin/env bash
# Use the same OS, architecture and browser locally and in CI.
set -euo pipefail
cd "$(dirname "$0")/.."
version=$(node -p 'require("./package.json").devDependencies["@playwright/test"]')
docker run --rm --init --platform linux/amd64 --ipc=host \
  -e TOMBO_VISUAL_CONTAINER=1 \
  -v "$PWD:/work" -v /work/node_modules -w /work \
  "mcr.microsoft.com/playwright:v${version}-noble" \
  bash -c 'npm ci --ignore-scripts && npm run test:visual:run -- "$@"' -- "$@"
