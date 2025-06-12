#!/usr/bin/env python3
"""
Spotify AI Music Recommendation Web App
A robust Flask application with proper error handling and startup checks.
"""

import os
import sys
import traceback
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from flask import Flask, render_template, request, jsonify
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'spotify-ai-recommendations-2024'

# Global variables to store loaded components
components_loaded = False
kmeans = None
pca = None
scaler_opt = None
scaler_tempo = None
df_pca = None
df_clean = None
top_features = None

def check_model_files():
    """Check if all required model files exist"""
    models_dir = parent_dir / 'models'
    required_files = [
        'kmeans_model.pkl',
        'pca_transformer.pkl',
        'standard_scaler.pkl',
        'minmax_scaler_tempo.pkl',
        'df_pca.pkl',
        'df_clean.pkl',
        'top_features.txt'
    ]

    missing_files = []
    for file in required_files:
        if not (models_dir / file).exists():
            missing_files.append(file)

    if missing_files:
        print("❌ Missing required model files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 To generate these files:")
        print("   1. Open notebooks/main.ipynb in Jupyter")
        print("   2. Run all cells to train models and save files")
        return False

    print("✅ All required model files found")
    return True

def load_ml_components():
    """Load ML components with proper error handling"""
    global components_loaded, kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features

    if components_loaded:
        return True

    try:
        # Check if model files exist first
        if not check_model_files():
            return False

        # Import and load components
        from recommendation_engine import load_components
        kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features = load_components()
        components_loaded = True
        print("✅ ML components loaded successfully")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure recommendation_engine.py is in the src directory")
        return False
    except Exception as e:
        print(f"❌ Error loading ML components: {e}")
        print(f"💡 Error details: {traceback.format_exc()}")
        return False

def get_popular_examples():
    """Get 3 random popular songs for examples"""
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
        {"song": "Viva La Vida", "artist": "Coldplay"}
    ]

    import random
    return random.sample(popular_songs, 3)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/popular-examples')
def popular_examples():
    """API endpoint for getting random popular song examples"""
    try:
        examples = get_popular_examples()
        return jsonify({
            'success': True,
            'examples': examples
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint for getting recommendations"""
    try:
        # Get form data
        data = request.get_json()
        song_name = data.get('song_name', '').strip()
        artist_name = data.get('artist_name', '').strip()
        playlist_size = int(data.get('playlist_size', 5))
        
        # Validate input
        if not song_name:
            return jsonify({
                'success': False,
                'error': 'Please enter a song name'
            })
        
        # Ensure playlist size is reasonable
        playlist_size = max(1, min(playlist_size, 20))
        
        # Import recommendation functions
        from recommendation_engine import recommend_from_name

        # Get recommendations
        if artist_name:
            recommendations = recommend_from_name(song_name, artist_name, playlist_size)
        else:
            recommendations = recommend_from_name(song_name, None, playlist_size)
        
        # Limit to requested playlist size
        if len(recommendations) > playlist_size:
            recommendations = recommendations.head(playlist_size)
        
        # Convert to list of dictionaries for JSON response
        recommendations_list = []
        for idx, row in recommendations.iterrows():
            recommendations_list.append({
                'track_name': row.get('track_name', 'Unknown Track'),
                'artist_name': row.get('artist_name', 'Unknown Artist'),
                'genre': row.get('genre', ''),
                'popularity': row.get('popularity', 0)
            })
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_list,
            'search_query': {
                'song_name': song_name,
                'artist_name': artist_name if artist_name else None,
                'playlist_size': playlist_size
            }
        })
        
    except Exception as e:
        print(f"Error in recommendation: {e}")
        print(traceback.format_exc())
        
        # Try fallback method
        try:
            if not components_loaded:
                load_ml_components()

            from recommendation_engine import manual_selection_fallback
            recommendations = manual_selection_fallback(df_pca, df_clean, song_name, artist_name, playlist_size)
            
            # Limit to requested playlist size
            if len(recommendations) > playlist_size:
                recommendations = recommendations.head(playlist_size)
            
            recommendations_list = []
            for idx, row in recommendations.iterrows():
                recommendations_list.append({
                    'track_name': row.get('track_name', 'Unknown Track'),
                    'artist_name': row.get('artist_name', 'Unknown Artist'),
                    'genre': row.get('genre', ''),
                    'popularity': row.get('popularity', 0)
                })
            
            return jsonify({
                'success': True,
                'recommendations': recommendations_list,
                'search_query': {
                    'song_name': song_name,
                    'artist_name': artist_name if artist_name else None,
                    'playlist_size': playlist_size
                },
                'note': 'Used fallback recommendation method'
            })
            
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            return jsonify({
                'success': False,
                'error': 'Unable to generate recommendations. Please try again with a different song.'
            })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        if not components_loaded:
            load_ml_components()
        
        return jsonify({
            'status': 'healthy',
            'components_loaded': components_loaded,
            'dataset_size': len(df_clean) if df_clean is not None else 0
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def start_app():
    """Start the Flask application with proper error handling"""
    print("🎵 Spotify AI Music Recommendation Web App")
    print("=" * 50)

    # Try to load ML components
    print("📦 Loading ML components...")
    if not load_ml_components():
        print("\n❌ Failed to load ML components")
        print("🔧 Please run the Jupyter notebook to generate model files first")
        return False

    # Find available port
    port = find_available_port()
    if not port:
        print("❌ No available ports found")
        return False

    print(f"🚀 Starting web server on port {port}...")
    print(f"🌐 Open your browser to: http://localhost:{port}")
    print("=" * 50)

    try:
        app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
        return True
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        return True
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        return False

if __name__ == '__main__':
    try:
        start_app()
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print(f"📋 Full error details:\n{traceback.format_exc()}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're in the correct directory")
        print("2. Run the Jupyter notebook to generate model files")
        print("3. Check that all dependencies are installed")
        sys.exit(1)
