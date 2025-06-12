#!/bin/bash

# Spotify AI Music Recommendation App - Quick Start Script

echo "🎵 Spotify AI Music Recommendation App"
echo "======================================"

# Function to print error messages
error_exit() {
    echo "❌ Error: $1"
    exit 1
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    error_exit "Python 3 is not installed or not in PATH. Please install Python 3.7 or higher."
fi
echo "✅ Python found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -d "src" ] || [ ! -f "src/web/app.py" ]; then
    error_exit "Please run this script from the project root directory (the one containing 'src' and 'requirements.txt')."
fi
echo "✅ Project structure verified"

# Create and activate virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment in '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR" || error_exit "Failed to create virtual environment."
fi

echo "🔧 Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate" || error_exit "Failed to activate virtual environment."

echo "📦 Installing/updating dependencies from requirements.txt..."
pip install -r requirements.txt || error_exit "Failed to install dependencies."

# Check for model files
MODELS_DIR="src/models"
REQUIRED_MODELS=(
    "kmeans_model.pkl"
    "pca_transformer.pkl"
    "standard_scaler.pkl"
    "minmax_scaler_tempo.pkl"
    "df_pca.pkl"
    "df_clean.pkl"
    "top_features.txt"
)
MISSING_MODELS=0
for model_file in "${REQUIRED_MODELS[@]}"; do
    if [ ! -f "$MODELS_DIR/$model_file" ]; then
        echo "   - Missing: $MODELS_DIR/$model_file"
        MISSING_MODELS=1
    fi
done

if [ "$MISSING_MODELS" -eq 1 ]; then
    echo "❌ Critical model files are missing."
    echo "💡 Please run the Jupyter notebook first to generate model files:"
    echo "   1. Navigate to the 'notebooks' directory."
    echo "   2. Open 'main.ipynb' in a Jupyter environment (e.g., Jupyter Lab, VS Code)."
    echo "   3. Run all cells in the notebook."
    echo "   This will create the necessary files in the '$MODELS_DIR' directory."
    exit 1
fi
echo "✅ Model files found"

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Attempting to use .env.example."
    if [ -f "config/.env.example" ]; then
        cp "config/.env.example" ".env"
        echo "✅ Copied config/.env.example to .env. Please review and update .env with your Spotify API credentials."
    else
        echo "❌ Error: config/.env.example not found. Cannot create .env file."
        echo "💡 Please create a .env file in the project root with your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET."
        exit 1
    fi
fi

# Launch the app
echo ""
echo "🚀 Starting the web application..."
echo "🌐 The app should open in your browser automatically if the Flask app is configured to do so."
echo "   If not, open http://localhost:5000 (or the port shown by Flask) in your browser."
echo "⏹️  Press Ctrl+C to stop the server."
echo ""

cd src/web
python3 app.py
