#!/bin/bash

# Instagram Account Creator Bot - Installation Script

echo "🤖 Instagram Account Creator Bot - Installation Script"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

# Make run script executable
chmod +x run.py

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🚀 To start the bot:"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "📱 Web interface will be available at: http://localhost:5000"
echo ""
echo "📖 For more information, see README.md"