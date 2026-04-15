# Test running script
# Usage: .\scripts\test.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Tests" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if running from project root
if (-not (Test-Path "manage.py")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

# Set Django settings module
$env:DJANGO_SETTINGS_MODULE = "student_management_system.settings.dev"

Write-Host "`n[1/1] Running Django tests..." -ForegroundColor Green
python manage.py test student_management_app --verbosity=2
if ($LASTEXITCODE -ne 0) {
    Write-Error "Tests failed"
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "All tests passed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
