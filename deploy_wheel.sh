#!/bin/bash

set -euo pipefail

REPOSITORY_URL="${1}"
DIST_DIR="${DIST_DIR:-dist}"

echo "==> Clearing previous builds"
rm -rf $DIST_DIR

echo "==> Building package (wheel + sdist)"
python3 -m build

echo "==> Checking package metadata"
twine check "$DIST_DIR"/*

echo "==> Uploading to repository"
twine upload --repository-url "$REPOSITORY_URL" "$DIST_DIR"/*

echo "==> Done"