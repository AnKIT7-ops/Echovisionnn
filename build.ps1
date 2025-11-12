param(
    [switch]$Clean
)

if ($Clean) {
    if (Test-Path -Path dist) { Remove-Item -Recurse -Force dist }
    if (Test-Path -Path build) { Remove-Item -Recurse -Force build }
    if (Test-Path -Path ConversationalGlasses.spec) { Remove-Item -Force ConversationalGlasses.spec }
}

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "Installing PyInstaller..."
    pip install pyinstaller | Out-Null
}

$common = @(
    '--noconfirm',
    '--onefile',
    '--name', 'ConversationalGlasses',
    '--add-data', 'yolov8n.pt;.',
    '--add-data', 'config.py;.',
    '--hidden-import', 'ultralytics',
    '--hidden-import', 'torch', '--hidden-import', 'torchvision', '--hidden-import', 'torchaudio',
    '--collect-all', 'ultralytics',
    '--collect-all', 'numpy',
    '--collect-all', 'cv2'
)

pyinstaller @common src/main.py

Write-Host "Build complete. See dist/ConversationalGlasses.exe"


