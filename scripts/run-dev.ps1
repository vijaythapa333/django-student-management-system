# Development server startup script
# Usage: .\scripts\run-dev.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Development Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if running from project root
if (-not (Test-Path "manage.py")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

# Set Django settings module
$env:DJANGO_SETTINGS_MODULE = "student_management_system.settings.dev"

Write-Host "`nEnvironment: Development" -ForegroundColor Yellow
Write-Host "Settings Module: $env:DJANGO_SETTINGS_MODULE" -ForegroundColor Yellow
Write-Host "`nStarting server..." -ForegroundColor Green

python manage.py runserver
