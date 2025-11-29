#!/bin/bash
# BlogFlow AI - ADK Setup and Launch Script

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              BlogFlow AI v2.0 Setup                      ║"
echo "║        Powered by Google ADK Framework                   ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Created .env file"
    else
        cat > .env << EOF
# Google API Key (required)
# Get your key from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_api_key_here

# Model configuration
GEMINI_MODEL=gemini-2.0-flash-exp

# Output directory
OUTPUT_DIR=output
EOF
        echo "✓ Created .env file with template"
    fi
    echo ""
    echo "📝 Please edit .env and add your GOOGLE_API_KEY"
    echo "   Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

# Check if API key is set
source .env
if [ "$GOOGLE_API_KEY" = "your_api_key_here" ] || [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ Error: GOOGLE_API_KEY not configured in .env file"
    echo "   Please edit .env and add your API key"
    exit 1
fi

echo "✓ API key configured"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📥 Installing dependencies (this may take a minute)..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✓ Dependencies installed"

# Create output directory
mkdir -p output

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                 Setup Complete! ✓                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Available commands:"
echo ""
echo "  1. Generate a blog article:"
echo "     python main_adk.py --topic \"Your Topic Here\""
echo ""
echo "  2. Start the ADK Web UI (interactive development):"
echo "     python main_adk.py --ui"
echo ""
echo "  3. Generate with interactive mode (see agent communication):"
echo "     python main_adk.py --topic \"Your Topic\" --interactive"
echo ""
echo "  4. Direct ADK commands (after activation):"
echo "     adk web --port 8000        # Start UI"
echo "     adk run agent              # Run agents"
echo "     adk eval agent             # Evaluate agents"
echo ""
echo "🌐 Web UI will be available at: http://localhost:8000"
echo ""

# Ask what to do
echo "What would you like to do?"
echo "  1) Generate a blog article"
echo "  2) Start the ADK Web UI"
echo "  3) Exit and run commands manually"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        read -p "Enter the blog topic: " topic
        python main_adk.py --topic "$topic"
        ;;
    2)
        echo ""
        echo "🌐 Starting ADK Web UI..."
        echo "   Access at: http://localhost:8000"
        echo "   Press Ctrl+C to stop"
        echo ""
        python main_adk.py --ui
        ;;
    3)
        echo ""
        echo "✓ Setup complete. Virtual environment is activated."
        echo "  Run commands as shown above."
        ;;
    *)
        echo ""
        echo "Invalid choice. Run ./start_adk.sh again to restart."
        ;;
esac
