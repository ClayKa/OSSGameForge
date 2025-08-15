# OSSGameForge Demo Script - Windows PowerShell
# Quickly start the application in demo mode

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting OSSGameForge Demo..." -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Visit: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is installed
try {
    $dockerComposeVersion = docker-compose --version
    Write-Host "✅ Docker Compose found: $dockerComposeVersion" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Docker Compose is not installed. It should come with Docker Desktop." -ForegroundColor Red
    Write-Host "Visit: https://docs.docker.com/compose/install/" -ForegroundColor Yellow
    exit 1
}

# Check if .env file exists, if not create from example
if (!(Test-Path ".env")) {
    Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

# Set demo mode environment variables
$env:MOCK_MODE = "true"
$env:USE_LOCAL_MODEL = "false"

Write-Host ""
Write-Host "🔧 Configuration:" -ForegroundColor Cyan
Write-Host "  - Mock Mode: Enabled"
Write-Host "  - Local Model: Disabled (using fallback)"
Write-Host ""

# Stop any existing containers
Write-Host "🧹 Cleaning up any existing containers..." -ForegroundColor Yellow
docker-compose down 2>$null

# Start the services
Write-Host "🐳 Starting Docker services..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend is healthy!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Backend might still be starting up..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✨ OSSGameForge Demo is running!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access points:" -ForegroundColor Cyan
Write-Host "  - API: http://localhost:8000"
Write-Host "  - API Documentation: http://localhost:8000/docs"
Write-Host "  - MinIO Console: http://localhost:9001"
Write-Host "    Username: minioadmin"
Write-Host "    Password: minioadmin"
Write-Host ""
Write-Host "📖 Quick Start Guide:" -ForegroundColor Cyan
Write-Host "  1. Visit the API docs to explore endpoints"
Write-Host "  2. Upload assets with user consent"
Write-Host "  3. Generate game scenes with AI"
Write-Host "  4. Export to HTML5 runner"
Write-Host ""
Write-Host "🛑 To stop the demo:" -ForegroundColor Yellow
Write-Host "  docker-compose down"
Write-Host ""
Write-Host "Happy game creation! 🎮" -ForegroundColor Green