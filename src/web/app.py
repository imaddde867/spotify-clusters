#!/usr/bin/env python3
"""
Spotify AI Music Recommendation Web App
A robust Flask application with proper error handling and startup checks.
"""

import os
import socket
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from flask import Flask, Response, jsonify, render_template, request

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", os.urandom(24).hex())

# Global variables to store loaded components
components_loaded = False
kmeans = None
pca = None
scaler_opt = None
scaler_tempo = None
df_pca = None
df_clean = None
top_features = None


def check_model_files() -> Tuple[bool, List[str]]:
    """
    Check if all required model files exist

    Returns:
        Tuple containing:
            - Boolean indicating if all files exist
            - List of missing files (empty if all files exist)
    """
    models_dir = parent_dir / "models"
    required_files = [
        "kmeans_model.pkl",
        "pca_transformer.pkl",
        "standard_scaler.pkl",
        "minmax_scaler_tempo.pkl",
        "df_pca.pkl",
        "df_clean.pkl",
        "top_features.txt",
    ]

    missing_files = [
        file for file in required_files if not (models_dir / file).exists()
    ]

    if missing_files:
        print("❌ Missing required model files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 To generate these files:")
        print("   1. Open notebooks/main.ipynb in Jupyter")
        print("   2. Run all cells to train models and save files")
        return False, missing_files

    print("✅ All required model files found")
    return True, []


def load_ml_components() -> Tuple[bool, Optional[str]]:
    """
    Load ML components with proper error handling

    Returns:
        Tuple containing:
            - Boolean indicating success
            - Error message if failed, None if successful
    """
    global components_loaded, kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features

    if components_loaded:
        return True, None

    try:
        files_exist, missing_files = check_model_files()
        if not files_exist:
            return False, f"Missing model files: {', '.join(missing_files)}"

        from recommendation_engine import load_components

        kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features = (
            load_components()
        )
        components_loaded = True
        print("✅ ML components loaded successfully")
        return True, None

    except ImportError as e:
        error_msg = f"Import error: {e}"
        print(f"❌ {error_msg}")
        print("💡 Make sure recommendation_engine.py is in the src directory")
        return False, error_msg
    except Exception as e:
        error_msg = f"Error loading ML components: {e}"
        print(f"❌ {error_msg}")
        print(f"💡 Error details: {traceback.format_exc()}")
        return False, error_msg


def get_popular_examples(count: int = 3) -> List[Dict[str, str]]:
    """
    Get random popular songs for examples

    Args:
        count: Number of examples to return

    Returns:
        List of dictionaries with song and artist names
    """
    popular_songs = [
        {"song": "Bohemian Rhapsody", "artist": "Queen"},
        {"song": "Billie Jean", "artist": "Michael Jackson"},
        {"song": "Hotel California", "artist": "Eagles"},
        {"song": "Imagine", "artist": "John Lennon"},
        {"song": "Sweet Child O' Mine", "artist": "Guns N' Roses"},
        {"song": "Stairway to Heaven", "artist": "Led Zeppelin"},
        {"song": "Smells Like Teen Spirit", "artist": "Nirvana"},
        {"song": "Like a Rolling Stone", "artist": "Bob Dylan"},
        {"song": "Purple Haze", "artist": "Jimi Hendrix"},
        {"song": "Good Vibrations", "artist": "The Beach Boys"},
        {"song": "Respect", "artist": "Aretha Franklin"},
        {"song": "Hey Jude", "artist": "The Beatles"},
        {"song": "What's Going On", "artist": "Marvin Gaye"},
        {"song": "Waterloo Sunset", "artist": "The Kinks"},
        {"song": "I Want to Hold Your Hand", "artist": "The Beatles"},
        {"song": "Dancing Queen", "artist": "ABBA"},
        {"song": "Superstition", "artist": "Stevie Wonder"},
        {"song": "Blinding Lights", "artist": "The Weeknd"},
        {"song": "Shape of You", "artist": "Ed Sheeran"},
        {"song": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars"},
        {"song": "Rolling in the Deep", "artist": "Adele"},
        {"song": "Someone Like You", "artist": "Adele"},
        {"song": "Lose Yourself", "artist": "Eminem"},
        {"song": "Crazy in Love", "artist": "Beyoncé"},
        {"song": "Halo", "artist": "Beyoncé"},
        {"song": "Umbrella", "artist": "Rihanna"},
        {"song": "Single Ladies", "artist": "Beyoncé"},
        {"song": "Bad Romance", "artist": "Lady Gaga"},
        {"song": "Poker Face", "artist": "Lady Gaga"},
        {"song": "Viva La Vida", "artist": "Coldplay"},
    ]

    import random

    count = min(count, len(popular_songs))
    return random.sample(popular_songs, count)


@app.route("/")
def index() -> str:
    """Main page"""
    # Check if ML components are loaded before rendering the page
    if not components_loaded:
        success, error_msg = load_ml_components()
        if not success:
            print(f"Warning: ML components not loaded: {error_msg}")
            # We'll still render the page, but the app will use fallback methods

    return render_template("index.html")


@app.route("/api/popular-examples")
def popular_examples() -> Response:
    """API endpoint for getting random popular song examples"""
    try:
        count = request.args.get("count", default=3, type=int)
        count = max(1, min(count, 5))  # Limit between 1 and 5

        examples = get_popular_examples(count)
        return jsonify({"success": True, "examples": examples})
    except Exception as e:
        print(f"Error getting popular examples: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/recommend", methods=["POST"])
def recommend() -> Response:
    """API endpoint for getting recommendations"""
    try:
        # Get and validate form data
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Input validation and sanitization
        song_name = data.get("song_name", "").strip()
        artist_name = data.get("artist_name", "").strip()
        
        # Validate playlist size with proper type checking
        try:
            playlist_size = int(data.get("playlist_size", 5))
        except (ValueError, TypeError):
            return jsonify({
                "success": False, 
                "error": "playlist_size must be a valid number"
            }), 400

        # Security: Validate input lengths to prevent abuse
        if len(song_name) > 200:
            return jsonify({
                "success": False, 
                "error": "Song name too long (max 200 characters)"
            }), 400
            
        if len(artist_name) > 200:
            return jsonify({
                "success": False, 
                "error": "Artist name too long (max 200 characters)"
            }), 400

        # Basic input validation
        if not song_name:
            return jsonify({
                "success": False, 
                "error": "Please enter a song name"
            }), 400
            
        if len(song_name) < 2:
            return jsonify({
                "success": False, 
                "error": "Song name must be at least 2 characters long"
            }), 400

        # Ensure playlist size is within reasonable bounds
        if playlist_size < 1 or playlist_size > 20:
            return jsonify({
                "success": False, 
                "error": "playlist_size must be between 1 and 20"
            }), 400

        # Ensure ML components are loaded
        if not components_loaded:
            success, error_msg = load_ml_components()
            if not success:
                print(f"Warning: Using fallback methods due to: {error_msg}")

        # Get recommendations
        from recommendation_engine import recommend_from_name

        recommendations = recommend_from_name(
            song_name, artist_name if artist_name else None, playlist_size
        )

        # Convert to list of dictionaries for JSON response
        recommendations_list = []
        for _, row in recommendations.iterrows():
            recommendations_list.append(
                {
                    "track_name": row.get("track_name", "Unknown Track"),
                    "artist_name": row.get("artist_name", "Unknown Artist"),
                    "genre": row.get("genre", ""),
                    "popularity": row.get("popularity", 0),
                }
            )

        return jsonify(
            {
                "success": True,
                "recommendations": recommendations_list,
                "search_query": {
                    "song_name": song_name,
                    "artist_name": artist_name if artist_name else None,
                    "playlist_size": playlist_size,
                },
            }
        )

    except Exception as e:
        print(f"Error in recommendation: {e}")
        print(traceback.format_exc())

        # Try fallback method
        try:
            if not components_loaded:
                success, _ = load_ml_components()
                if not success:
                    print(
                        "Warning: Components still not loaded, using minimal fallback"
                    )

            from recommendation_engine import manual_selection_fallback

            recommendations = manual_selection_fallback(
                df_pca, df_clean, song_name, artist_name, playlist_size
            )

            recommendations_list = []
            for _, row in recommendations.iterrows():
                recommendations_list.append(
                    {
                        "track_name": row.get("track_name", "Unknown Track"),
                        "artist_name": row.get("artist_name", "Unknown Artist"),
                        "genre": row.get("genre", ""),
                        "popularity": row.get("popularity", 0),
                    }
                )

            return jsonify(
                {
                    "success": True,
                    "recommendations": recommendations_list,
                    "search_query": {
                        "song_name": song_name,
                        "artist_name": artist_name if artist_name else None,
                        "playlist_size": playlist_size,
                    },
                    "note": "Used fallback recommendation method",
                }
            )

        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Unable to generate recommendations. Please try again with a different song.",
                    }
                ),
                500,
            )


@app.route("/health")
def health_check() -> Response:
    """Health check endpoint"""
    try:
        status_info = {
            "status": "healthy",
            "components_loaded": components_loaded,
            "python_version": sys.version,
            "timestamp": pd.Timestamp.now().isoformat(),
        }

        if not components_loaded:
            success, error_msg = load_ml_components()
            if not success:
                status_info["status"] = "degraded"
                status_info["message"] = f"Failed to load ML components: {error_msg}"
                return jsonify(status_info), 503  # Service Unavailable

        return jsonify(status_info)
    except Exception as e:
        error_info = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc(),
        }
        return jsonify(error_info), 500


def find_available_port(start_port: int = 5000, max_attempts: int = 10) -> int:
    """
    Find an available port to run the Flask app

    Args:
        start_port: Port number to start checking from
        max_attempts: Maximum number of ports to check

    Returns:
        Available port number

    Raises:
        RuntimeError: If no available port is found
    """
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
                return port
        except OSError:
            continue
    raise RuntimeError(
        f"Could not find an available port after {max_attempts} attempts"
    )


def start_app() -> None:
    """Start the Flask application"""
    try:
        # Try to load ML components, but continue even if it fails
        success, error_msg = load_ml_components()
        if not success:
            print(f"⚠️ Warning: ML components not loaded: {error_msg}")
            print("⚠️ The application will use fallback methods for recommendations")

        # Determine environment
        flask_env = os.getenv("FLASK_ENV", "production")
        debug_mode = flask_env == "development"

        # Find available port
        start_port = 5001 if debug_mode else 5000
        port = find_available_port(start_port=start_port)

        # Start server
        print(f"🚀 Starting server on port {port} in {flask_env} mode")
        app.run(host="0.0.0.0", port=port, debug=debug_mode)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    start_app()
