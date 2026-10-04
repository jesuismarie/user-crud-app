#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/app"

cd "$APP_DIR/backend"

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pip install pip-audit
pip-audit -r requirements.txt
pytest -v
