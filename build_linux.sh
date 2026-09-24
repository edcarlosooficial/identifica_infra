#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install -r requirements.txt
python3 -m PyInstaller --noconfirm --clean --onefile --name mareo-identifica-infra-free mareo_mapper.py
echo "Build: dist/mareo-identifica-infra-free"
