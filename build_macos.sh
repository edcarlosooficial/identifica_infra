#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m PyInstaller --noconfirm --clean --onefile --name mareo-identifica-infra-free-macos mareo_mapper.py
echo "Build criado em dist/mareo-identifica-infra-free-macos"
