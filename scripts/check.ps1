# Code quality check script (format + lint + test)
# Usage: .\scripts\check.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Full Code Quality Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if running from project root
if (-not (Test-Path "manage.py")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

$env:DJANGO_SETTINGS_MODULE = "student_management_system.settings.dev"

Write-Host "`n[1/4] Checking code formatting with Black..." -ForegroundColor Green
python -m black --check student_management_app student_management_system --config pyproject.toml
if ($LASTEXITCODE -ne 0) {
    Write-Error "Code is not formatted. Run '.\scripts\format.ps1' to fix."
    exit 1
}

Write-Host "`n[2/4] Checking import order with isort..." -ForegroundColor Green
python -m isort --check-only student_management_app student_management_system --settings-path pyproject.toml
if ($LASTEXITCODE -ne 0) {
    Write-Error "Imports are not sorted. Run '.\scripts\format.ps1' to fix."
    exit 1
}

Write-Host "`n[3/4] Running Flake8 linting..." -ForegroundColor Green
python -m flake8 student_management_app student_management_system --config .flake8
if ($LASTEXITCODE -ne 0) {
    Write-Error "Linting failed"
    exit 1
}

Write-Host "`n[4/4] Running tests..." -ForegroundColor Green
python manage.py test student_management_app --verbosity=1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Tests failed"
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "All checks passed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
