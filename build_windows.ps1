$ErrorActionPreference="Stop"
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --name Mareo_Identifica_Infra_FREE mareo_gui.py
Write-Host "Build: dist\Mareo_Identifica_Infra_FREE.exe"
