#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

if [ -z "${UV_PUBLISH_TOKEN:-}" ]; then
  printf "Enter PyPI token (UV_PUBLISH_TOKEN): "
  read -r UV_PUBLISH_TOKEN
fi

if [ -z "${UV_PUBLISH_TOKEN:-}" ]; then
  echo "ERROR: no token provided."
  exit 1
fi

echo "Building package..."
uv build

echo "Publishing to PyPI..."
uv publish

echo "Done."
