# Project setup script
# Usage: .\scripts\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if running from project root
if (-not (Test-Path "manage.py")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

Write-Host "`n[1/5] Installing dependencies..." -ForegroundColor Green
pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies"
    exit 1
}

Write-Host "`n[2/5] Creating logs directory..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

Write-Host "`n[3/5] Running migrations..." -ForegroundColor Green
$env:DJANGO_SETTINGS_MODULE = "student_management_system.settings.dev"
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Error "Migrations failed"
    exit 1
}

Write-Host "`n[4/5] Running code formatters..." -ForegroundColor Green
python -m black student_management_app student_management_system --config pyproject.toml
python -m isort student_management_app student_management_system --settings-path pyproject.toml

Write-Host "`n[5/5] Running tests..." -ForegroundColor Green
python manage.py test student_management_app --verbosity=1
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Some tests failed, but setup is complete"
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Update .env file with your configuration" -ForegroundColor Yellow
Write-Host "  2. Run '.\scripts\run-dev.ps1' to start the development server" -ForegroundColor Yellow
