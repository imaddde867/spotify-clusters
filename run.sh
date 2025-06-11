#!/bin/bash

# Spotify AI Music Recommendation App - Quick Start Script

echo "🎵 Spotify AI Music Recommendation App"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "💡 Please install Python 3.7 or higher"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -d "src" ] || [ ! -f "src/web/app.py" ]; then
    echo "❌ Please run this script from the project root directory"
    echo "💡 Make sure you can see the 'src' folder"
    exit 1
fi

echo "✅ Project structure verified"

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Check for model files
if [ ! -f "src/models/kmeans_model.pkl" ]; then
    echo "❌ Model files not found"
    echo "💡 Please run the Jupyter notebook first to generate model files"
    echo "   1. Open notebooks/main.ipynb"
    echo "   2. Run all cells"
    exit 1
fi

echo "✅ Model files found"

# Launch the app
echo ""
echo "🚀 Starting the web application..."
echo "🌐 The app will open in your browser automatically"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

cd src/web
python3 app.py
