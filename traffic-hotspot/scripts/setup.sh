#!/bin/bash

# Traffic Hotspot Predictor Setup Script
# This script sets up the development environment

echo "🚦 Setting up Traffic Hotspot Predictor..."
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd web
npm install

if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed successfully"
else
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

cd ..

# Create data directories if they don't exist
echo "📁 Creating data directories..."
mkdir -p data/raw data/processed ml/models

echo "✅ Data directories created"

# Check if raw data files exist
echo "📊 Checking for raw data files..."
if [ ! -f "data/raw/svc_raw_data_class_2020_2024.csv" ]; then
    echo "⚠️  SVC data file not found: data/raw/svc_raw_data_class_2020_2024.csv"
    echo "   Please download it from Toronto Open Data Portal and place it in data/raw/"
fi

if [ ! -f "data/raw/comptages_vehicules_cyclistes_pietons.csv" ]; then
    echo "⚠️  Intersection data file not found: data/raw/comptages_vehicules_cyclistes_pietons.csv"
    echo "   Please download it from Toronto Open Data Portal and place it in data/raw/"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Download the raw data files from Toronto Open Data Portal"
echo "2. Run: python ml/clean_svc.py"
echo "3. Run: python ml/clean_counts.py"
echo "4. Run: python ml/train.py"
echo "5. Start the API: cd api && python main.py"
echo "6. Start the frontend: cd web && npm run dev"
echo ""
echo "📚 See README.md for detailed instructions"

