#!/usr/bin/env bash
#
# deploy.sh — Build the Jupyter Book and publish it to the gh-pages branch.
#
# Why this script exists:
#   The book enables thebe-lite live code execution (use_thebe_lite: true in
#   _config.yml). That feature bundles the entire working directory into
#   _build/html so cells can run in-browser, and it ignores Sphinx
#   exclude_patterns. As a result _build/html ends up containing .git/,
#   .figvenv/, data/, etc. Pushing that directly with ghp-import fails because
#   `git fast-import` rejects nested .git/ paths. This script builds, then
#   copies only the real site files into a staging dir before publishing.
#
# Usage:
#   ./deploy.sh
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

VENV="${VENV:-.figvenv}"
BUILD_DIR="_build/html"
STAGE_DIR="$(mktemp -d -t ghpages_stage.XXXXXX)"

cleanup() { rm -rf "$STAGE_DIR"; }
trap cleanup EXIT

echo "==> Activating virtualenv: $VENV"
# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "==> Ensuring ghp-import is installed"
python -m pip show ghp-import >/dev/null 2>&1 || python -m pip install ghp-import

echo "==> Clean build"
rm -rf _build
jupyter-book build . --all

echo "==> Staging filtered site (stripping repo/venv junk)"
rsync -a \
  --exclude '.git' \
  --exclude '.figvenv' \
  --exclude '.venv' \
  --exclude 'causal_venv' \
  --exclude '.cursor' \
  --exclude '.vscode' \
  --exclude '.gitignore' \
  --exclude 'requirements.txt' \
  --exclude '__pycache__' \
  --exclude '.DS_Store' \
  --exclude '.ipynb_checkpoints' \
  "$BUILD_DIR"/ "$STAGE_DIR"/

echo "==> Deploying to gh-pages"
# -n: add .nojekyll so _static/_images are served; -p: push; -f: force
ghp-import -n -p -f -m "Deploy Jupyter Book to GitHub Pages" "$STAGE_DIR"

echo "==> Done. Published to the gh-pages branch."
