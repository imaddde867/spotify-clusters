#!/usr/bin/env python3
"""
Spotify AI Recommendation App Launcher
Handles all startup checks and launches the web app reliably.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'pandas', 
        'numpy',
        'scikit-learn',
        'spotipy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_model_files():
    """Check if ML model files exist"""
    models_dir = Path('src/models')
    required_files = [
        'kmeans_model.pkl',
        'pca_transformer.pkl',
        'standard_scaler.pkl',
        'minmax_scaler_tempo.pkl',
        'df_pca.pkl',
        'df_clean.pkl',
        'top_features.txt'
    ]
    
    if not models_dir.exists():
        print("❌ Models directory not found")
        print("💡 Make sure you're running from the project root directory")
        return False
    
    missing_files = []
    for file in required_files:
        if not (models_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing model files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Generate model files by:")
        print("   1. Opening notebooks/main.ipynb in Jupyter")
        print("   2. Running all cells to train and save models")
        return False
    
    print("✅ All model files found")
    return True

def check_directory_structure():
    """Check if we're in the right directory"""
    required_dirs = ['src', 'src/web', 'src/models']
    required_files = ['src/web/app.py', 'src/recommendation_engine.py']
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Directory not found: {dir_path}")
            print("💡 Make sure you're in the project root directory")
            return False
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            return False
    
    print("✅ Project structure is correct")
    return True

def launch_app():
    """Launch the Flask application"""
    print("\n🚀 Launching Spotify AI Recommendation App...")
    print("=" * 50)
    
    try:
        # Change to web directory and run app
        os.chdir('src/web')
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ App failed to start: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🎵 Spotify AI Music Recommendation App Launcher")
    print("=" * 50)
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Model Files", check_model_files)
    ]
    
    print("🔍 Running startup checks...")
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        if not check_func():
            print(f"\n💥 Startup failed at: {check_name}")
            print("🔧 Please fix the issues above and try again")
            return False
    
    print("\n✅ All checks passed!")
    
    # Launch the app
    return launch_app()

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Startup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error during startup: {e}")
        sys.exit(1)
