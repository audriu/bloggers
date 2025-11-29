#!/bin/bash
# Setup script for BlogFlow AI

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         BlogFlow AI - Installation Script               ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment (default: yes)
read -p "Create virtual environment in .venv? (recommended) (Y/n): " create_venv

if [ "$create_venv" != "n" ] && [ "$create_venv" != "N" ]; then
    echo "Creating virtual environment in .venv/..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
    echo ""
    
    echo "Activating virtual environment..."
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Setup .env file
if [ ! -f .env ]; then
    echo "Setting up .env file..."
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    
    echo "⚠️  IMPORTANT: You need to add your Google API key!"
    echo ""
    echo "Steps:"
    echo "  1. Visit: https://aistudio.google.com/app/apikey"
    echo "  2. Create an API key"
    echo "  3. Edit .env file and paste your key"
    echo ""
    read -p "Press Enter to open .env file in nano editor (or edit manually later)..."
    nano .env || vim .env || echo "Please edit .env file manually"
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create output directory
echo "Creating output directory..."
mkdir -p output
echo "✓ Output directory created"
echo ""

# Test installation
echo "Testing installation..."
if python3 -c "import google.genai; import dotenv; import colorama" 2>/dev/null; then
    echo "✓ All dependencies import successfully"
else
    echo "✗ Dependency import failed"
    exit 1
fi
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║            Installation Complete! 🎉                     ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

echo "Next steps:"
if [ "$create_venv" != "n" ] && [ "$create_venv" != "N" ]; then
    echo "  1. Activate virtual environment: source .venv/bin/activate"
    echo "  2. Make sure your API key is in the .env file"
    echo "  3. Run demo: python3 demo.py"
    echo "  4. Generate article: python3 main.py --topic \"Your Topic\""
else
    echo "  1. Make sure your API key is in the .env file"
    echo "  2. Run demo: python3 demo.py"
    echo "  3. Generate article: python3 main.py --topic \"Your Topic\""
fi
echo ""

if [ "$create_venv" != "n" ] && [ "$create_venv" != "N" ]; then
    echo "Note: To activate the virtual environment in future sessions:"
    echo "  source .venv/bin/activate"
    echo ""
fi

echo "For more info, see:"
echo "  • README.md - Full documentation"
echo "  • QUICKSTART.md - Quick start guide"
echo "  • ARCHITECTURE.md - Technical details"
echo ""
