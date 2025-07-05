#!/usr/bin/env python3
"""
Development server with enhanced features for the Spotify AI system.

This script provides a development server with:
- Auto-reload on file changes
- Performance monitoring
- Enhanced logging
- Health checks
- Debug tools

Usage: python scripts/dev/dev_server.py [--port PORT] [--debug]
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from utils.logging_config import setup_logging, get_logger
from utils.performance import log_system_metrics, SystemMetrics


def setup_development_environment():
    """Set up development environment variables and logging."""
    # Set development environment variables
    os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_DEBUG"] = "1"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    # Setup enhanced logging for development
    logger = setup_logging(
        log_level="DEBUG",
        log_file="dev_server.log",
        log_dir="logs",
        console_output=True
    )
    
    return logger


def check_dependencies():
    """Check if all required dependencies are available."""
    logger = get_logger("dev_server")
    
    required_packages = [
        "flask", "pandas", "numpy", "sklearn", 
        "joblib", "spotipy", "psutil"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.debug(f"✅ {package} is available")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"❌ {package} is missing")
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.error("Please run: pip install -r requirements.txt")
        return False
    
    logger.info("✅ All dependencies are available")
    return True


def check_model_files():
    """Check if ML model files are available."""
    logger = get_logger("dev_server")
    
    models_dir = src_path / "models"
    required_files = [
        "kmeans_model.pkl",
        "pca_transformer.pkl", 
        "standard_scaler.pkl",
        "minmax_scaler_tempo.pkl",
        "df_pca.pkl",
        "df_clean.pkl",
        "top_features.txt"
    ]
    
    missing_files = []
    
    for file_name in required_files:
        file_path = models_dir / file_name
        if file_path.exists():
            logger.debug(f"✅ {file_name} found")
        else:
            missing_files.append(file_name)
            logger.warning(f"❌ {file_name} missing")
    
    if missing_files:
        logger.warning(f"Missing model files: {', '.join(missing_files)}")
        logger.warning("The app will use fallback methods for recommendations")
        return False
    
    logger.info("✅ All model files are available")
    return True


def start_development_server(port: int = 5001, debug: bool = True):
    """Start the development server with enhanced features."""
    logger = get_logger("dev_server")
    
    logger.info(f"🚀 Starting Spotify AI Development Server on port {port}")
    
    # Log system metrics
    logger.info("📊 System Metrics:")
    log_system_metrics()
    
    # Check environment
    if not check_dependencies():
        logger.error("❌ Dependency check failed")
        sys.exit(1)
    
    model_files_ok = check_model_files()
    if not model_files_ok:
        logger.warning("⚠️ Model files missing - continuing with fallback methods")
    
    # Import and start Flask app
    try:
        from web.app import app, find_available_port
        
        # Find available port
        actual_port = find_available_port(start_port=port)
        if actual_port != port:
            logger.info(f"Port {port} not available, using {actual_port}")
        
        # Configure Flask for development
        app.config["DEBUG"] = debug
        app.config["TESTING"] = False
        
        # Add development routes
        @app.route("/dev/health")
        def dev_health():
            """Development health check endpoint."""
            metrics = SystemMetrics.get_all_metrics()
            return {
                "status": "ok",
                "environment": "development",
                "debug": debug,
                "model_files_available": model_files_ok,
                "system_metrics": metrics
            }
        
        @app.route("/dev/metrics")
        def dev_metrics():
            """Development metrics endpoint."""
            return SystemMetrics.get_all_metrics()
        
        logger.info(f"🌐 Server will be available at:")
        logger.info(f"   - Main app: http://localhost:{actual_port}")
        logger.info(f"   - Health check: http://localhost:{actual_port}/dev/health")
        logger.info(f"   - Metrics: http://localhost:{actual_port}/dev/metrics")
        logger.info(f"   - API health: http://localhost:{actual_port}/health")
        
        # Start the server
        app.run(
            host="0.0.0.0",
            port=actual_port,
            debug=debug,
            use_reloader=True,
            use_debugger=debug
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Start development server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=5001, 
        help="Port to run the server on (default: 5001)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        default=True,
        help="Enable debug mode (default: True)"
    )
    parser.add_argument(
        "--no-debug", 
        action="store_true",
        help="Disable debug mode"
    )
    
    args = parser.parse_args()
    
    # Setup development environment
    logger = setup_development_environment()
    
    # Determine debug mode
    debug_mode = args.debug and not args.no_debug
    
    logger.info("🔧 Development Environment Setup Complete")
    logger.info(f"   - Debug mode: {debug_mode}")
    logger.info(f"   - Port: {args.port}")
    logger.info(f"   - Log level: DEBUG")
    
    # Start server
    start_development_server(port=args.port, debug=debug_mode)


if __name__ == "__main__":
    main()