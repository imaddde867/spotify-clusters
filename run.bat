@echo off
REM Spotify AI Music Recommendation App - Windows Quick Start Script

echo 🎵 Spotify AI Music Recommendation App
echo ======================================

REM Function-like label for error handling
:error_exit
    echo ❌ Error: %~1
    pause
    exit /b 1

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    call :error_exit "Python is not installed or not in PATH. Please install Python 3.7 or higher from python.org"
)
echo ✅ Python found
python --version

REM Check if we're in the right directory
if not exist "src" ( call :error_exit "Please run this script from the project root directory (the one containing 'src' and 'requirements.txt')." )
if not exist "src\web\app.py" ( call :error_exit "app.py not found in src\web\. Please check your project structure." )
echo ✅ Project structure verified

REM Create and activate virtual environment
set "VENV_DIR=venv"
if not exist "%VENV_DIR%" (
    echo 📦 Creating virtual environment in '%VENV_DIR%'...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 ( call :error_exit "Failed to create virtual environment." )
)

echo 🔧 Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 ( call :error_exit "Failed to activate virtual environment." )

echo 📦 Installing/updating dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 ( call :error_exit "Failed to install dependencies." )

REM Check for model files
set "MODELS_DIR=src\models"
set "MISSING_MODELS=0"

REM Check each model file
if not exist "%MODELS_DIR%\kmeans_model.pkl" ( echo    - Missing: %MODELS_DIR%\kmeans_model.pkl & set "MISSING_MODELS=1" )
if not exist "%MODELS_DIR%\pca_transformer.pkl" ( echo    - Missing: %MODELS_DIR%\pca_transformer.pkl & set "MISSING_MODELS=1" )
if not exist "%MODELS_DIR%\standard_scaler.pkl" ( echo    - Missing: %MODELS_DIR%\standard_scaler.pkl & set "MISSING_MODELS=1" )
if not exist "%MODELS_DIR%\minmax_scaler_tempo.pkl" ( echo    - Missing: %MODELS_DIR%\minmax_scaler_tempo.pkl & set "MISSING_MODELS=1" )
if not exist "%MODELS_DIR%\df_pca.pkl" ( echo    - Missing: %MODELS_DIR%\df_pca.pkl & set "MISSING_MODELS=1" )
if not exist "%MODELS_DIR%\df_clean.pkl" ( echo    - Missing: %MODELS_DIR%\df_clean.pkl & set "MISSING_MODELS=1" )
if not exist "%MODELS_DIR%\top_features.txt" ( echo    - Missing: %MODELS_DIR%\top_features.txt & set "MISSING_MODELS=1" )

if "%MISSING_MODELS%" == "1" (
    echo ❌ Critical model files are missing.
    echo 💡 Please run the Jupyter notebook first to generate model files:
    echo    1. Navigate to the 'notebooks' directory.
    echo    2. Open 'main.ipynb' in a Jupyter environment (e.g., Jupyter Lab, VS Code).
    echo    3. Run all cells in the notebook.
    echo    This will create the necessary files in the '%MODELS_DIR%' directory.
    pause
    exit /b 1
)
echo ✅ Model files found

REM Check for .env file
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Attempting to use .env.example.
    if exist "config\.env.example" (
        copy "config\.env.example" ".env" >nul
        echo ✅ Copied config\.env.example to .env. Please review and update .env with your Spotify API credentials.
    ) else (
        echo ❌ Error: config\.env.example not found. Cannot create .env file.
        echo 💡 Please create a .env file in the project root with your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.
        pause
        exit /b 1
    )
)

REM Launch the app
echo.
echo 🚀 Starting the web application...
echo 🌐 The app should open in your browser automatically if the Flask app is configured to do so.
echo    If not, open http://localhost:5000 (or the port shown by Flask) in your browser.
echo ⏹️  Press Ctrl+C to stop the server.
echo.

cd src\web
python app.py

pause
