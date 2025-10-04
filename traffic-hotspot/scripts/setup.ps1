# Traffic Hotspot Predictor Setup Script for Windows PowerShell
# This script sets up the development environment

Write-Host "🚦 Setting up Traffic Hotspot Predictor..." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Node.js not found"
    }
    Write-Host "✅ Node.js is installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18+ first." -ForegroundColor Red
    Write-Host "   Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Blue
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

# Install frontend dependencies
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Blue
Set-Location web
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    exit 1
}

Set-Location ..

# Create data directories if they don't exist
Write-Host "📁 Creating data directories..." -ForegroundColor Blue
New-Item -ItemType Directory -Path "data\raw", "data\processed", "ml\models" -Force | Out-Null

Write-Host "✅ Data directories created" -ForegroundColor Green

# Check if raw data files exist
Write-Host "📊 Checking for raw data files..." -ForegroundColor Blue
if (-not (Test-Path "data\raw\svc_raw_data_class_2020_2024.csv")) {
    Write-Host "⚠️  SVC data file not found: data\raw\svc_raw_data_class_2020_2024.csv" -ForegroundColor Yellow
    Write-Host "   Please download it from Toronto Open Data Portal and place it in data\raw\" -ForegroundColor Yellow
}

if (-not (Test-Path "data\raw\comptages_vehicules_cyclistes_pietons.csv")) {
    Write-Host "⚠️  Intersection data file not found: data\raw\comptages_vehicules_cyclistes_pietons.csv" -ForegroundColor Yellow
    Write-Host "   Please download it from Toronto Open Data Portal and place it in data\raw\" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Download the raw data files from Toronto Open Data Portal" -ForegroundColor White
Write-Host "2. Run: python ml\clean_svc.py" -ForegroundColor White
Write-Host "3. Run: python ml\clean_counts.py" -ForegroundColor White
Write-Host "4. Run: python ml\train.py" -ForegroundColor White
Write-Host "5. Start the API: cd api && python main.py" -ForegroundColor White
Write-Host "6. Start the frontend: cd web && npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "📚 See README.md for detailed instructions" -ForegroundColor Cyan

