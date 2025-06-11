#!/usr/bin/env python3
"""
Spotify AI Music Recommendation Web App Launcher
This script helps users easily start the web application with proper checks.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_required_files():
    """Check if all required model files exist"""
    required_files = [
        'models/kmeans_model.pkl',
        'models/pca_transformer.pkl', 
        'models/standard_scaler.pkl',
        'models/minmax_scaler_tempo.pkl',
        'models/df_pca.pkl',
        'models/df_clean.pkl',
        'models/top_features.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required model files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 To generate these files:")
        print("   1. Open main.ipynb in Jupyter")
        print("   2. Run all cells to train models and save files")
        return False
    
    print("✅ All required model files found")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'flask': 'flask',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'scikit-learn': 'sklearn',  # scikit-learn imports as sklearn
        'joblib': 'joblib'
    }
    missing_packages = []

    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages:")
        print("   pip install -r requirements.txt")
        return False

    print("✅ All required packages installed")
    return True

def check_env_file():
    """Check for environment file and provide guidance"""
    if Path('.env').exists():
        print("✅ Environment file (.env) found")
        return True
    else:
        print("⚠️  No .env file found (optional for Spotify API)")
        print("💡 To enable Spotify API:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your Spotify API credentials")
        print("   3. Get credentials from: https://developer.spotify.com/dashboard/")
        print("   Note: App works without Spotify API using fallback mode")
        return True

def start_webapp():
    """Start the Flask web application"""
    print("\n🚀 Starting Spotify AI Music Recommendation Web App...")
    print("📱 Open your browser and go to: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Web app stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting web app: {e}")
        print("💡 Try running: python app.py")

def main():
    """Main function to run all checks and start the app"""
    print("🎵 Spotify AI Music Recommendation Web App")
    print("=" * 50)
    
    # Run all checks
    checks = [
        check_python_version(),
        check_required_files(),
        check_dependencies(),
        check_env_file()
    ]
    
    if all(checks):
        print("\n✅ All checks passed!")
        start_webapp()
    else:
        print("\n❌ Some checks failed. Please fix the issues above before running the app.")
        sys.exit(1)

if __name__ == "__main__":
    main()
