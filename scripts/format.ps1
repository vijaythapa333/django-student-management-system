# Code formatting script
# Usage: .\scripts\format.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Code Formatters" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if running from project root
if (-not (Test-Path "manage.py")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

Write-Host "`n[1/2] Running Black formatter..." -ForegroundColor Green
python -m black student_management_app student_management_system --config pyproject.toml
if ($LASTEXITCODE -ne 0) {
    Write-Error "Black formatting failed"
    exit 1
}

Write-Host "`n[2/2] Running isort..." -ForegroundColor Green
python -m isort student_management_app student_management_system --settings-path pyproject.toml
if ($LASTEXITCODE -ne 0) {
    Write-Error "isort failed"
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Code formatting completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
