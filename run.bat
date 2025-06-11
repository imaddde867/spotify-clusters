@echo off
REM Spotify AI Music Recommendation App - Windows Quick Start Script

echo 🎵 Spotify AI Music Recommendation App
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if we're in the right directory
if not exist "src" (
    echo ❌ Please run this script from the project root directory
    echo 💡 Make sure you can see the 'src' folder
    pause
    exit /b 1
)

if not exist "src\web\app.py" (
    echo ❌ app.py not found in src\web\
    echo 💡 Please check your project structure
    pause
    exit /b 1
)

echo ✅ Project structure verified

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Installing/updating dependencies...
pip install -r requirements.txt

REM Check for model files
if not exist "src\models\kmeans_model.pkl" (
    echo ❌ Model files not found
    echo 💡 Please run the Jupyter notebook first to generate model files
    echo    1. Open notebooks\main.ipynb
    echo    2. Run all cells
    pause
    exit /b 1
)

echo ✅ Model files found

REM Launch the app
echo.
echo 🚀 Starting the web application...
echo 🌐 The app will open in your browser automatically
echo ⏹️  Press Ctrl+C to stop the server
echo.

cd src\web
python app.py

pause
