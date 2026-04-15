# Code linting script
# Usage: .\scripts\lint.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Code Linters" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if running from project root
if (-not (Test-Path "manage.py")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

Write-Host "`n[1/1] Running Flake8..." -ForegroundColor Green
python -m flake8 student_management_app student_management_system --config .flake8
if ($LASTEXITCODE -ne 0) {
    Write-Error "Flake8 linting failed"
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Code linting completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
