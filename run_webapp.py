#!/usr/bin/env python3
"""
Clean Web App Launcher for Organized Repository
This script launches the web app from the new organized structure.
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

def check_project_structure():
    """Check if the project has been organized"""
    required_paths = [
        'src/recommendation_engine.py',
        'src/web/app.py',
        'src/models',
        'src/web/templates/index.html'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
    
    if missing_paths:
        print("❌ Project structure not organized. Missing:")
        for path in missing_paths:
            print(f"   - {path}")
        print("\n💡 Run the cleanup script first:")
        print("   python cleanup_and_organize.py")
        return False
    
    print("✅ Project structure is organized")
    return True

def check_required_files():
    """Check if all required model files exist"""
    required_files = [
        'src/models/kmeans_model.pkl',
        'src/models/pca_transformer.pkl', 
        'src/models/standard_scaler.pkl',
        'src/models/minmax_scaler_tempo.pkl',
        'src/models/df_pca.pkl',
        'src/models/df_clean.pkl',
        'src/models/top_features.txt'
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
        print("   1. Open notebooks/main.ipynb in Jupyter")
        print("   2. Run all cells to train models and save files")
        print("   3. Run cleanup script: python cleanup_and_organize.py")
        return False
    
    print("✅ All required model files found")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'flask': 'flask',
        'pandas': 'pandas', 
        'numpy': 'numpy',
        'scikit-learn': 'sklearn',
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
    env_paths = ['.env', 'config/.env']
    env_found = any(Path(path).exists() for path in env_paths)
    
    if env_found:
        print("✅ Environment file found")
        return True
    else:
        print("⚠️  No .env file found (optional for Spotify API)")
        print("💡 To enable Spotify API:")
        print("   1. Copy config/.env.example to .env")
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
        # Change to src/web directory and run the app
        os.chdir('src/web')
        
        # Add src directory to Python path so imports work
        src_path = os.path.abspath('..')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5001)
        
    except KeyboardInterrupt:
        print("\n👋 Web app stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting web app: {e}")
        print("💡 Try running from project root:")
        print("   cd src/web && python app.py")

def show_project_info():
    """Show information about the organized project"""
    print("\n📁 Organized Project Structure:")
    print("   src/recommendation_engine.py  - Core ML engine")
    print("   src/web/app.py               - Flask web server")
    print("   src/models/                  - Trained ML models")
    print("   notebooks/main.ipynb         - Original analysis")
    print("   data/spotify_data.csv        - Dataset")
    print("   docs/                        - Documentation")
    
    print("\n🎯 Features:")
    print("   • AI-powered music recommendations")
    print("   • PCA + K-means clustering (35 clusters)")
    print("   • 1.1M+ Spotify tracks dataset")
    print("   • Modern responsive web interface")
    print("   • Spotify API integration with fallback")

def main():
    """Main function to run all checks and start the app"""
    print("🎵 Spotify AI Music Recommendation Web App (Clean Version)")
    print("=" * 60)
    
    # Check if project is organized
    if not check_project_structure():
        print("\n❌ Please organize the project first by running:")
        print("   python cleanup_and_organize.py")
        sys.exit(1)
    
    # Run all checks
    checks = [
        check_python_version(),
        check_required_files(),
        check_dependencies(),
        check_env_file()
    ]
    
    if all(checks):
        print("\n✅ All checks passed!")
        show_project_info()
        start_webapp()
    else:
        print("\n❌ Some checks failed. Please fix the issues above before running the app.")
        sys.exit(1)

if __name__ == "__main__":
    main()
