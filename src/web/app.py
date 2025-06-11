from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import traceback
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recommendation_engine import recommend_from_name, manual_selection_fallback, load_components
import os

app = Flask(__name__)

# Global variables to store loaded components
components_loaded = False
kmeans = None
pca = None
scaler_opt = None
scaler_tempo = None
df_pca = None
df_clean = None
top_features = None

def load_ml_components():
    """Load ML components once at startup"""
    global components_loaded, kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features
    
    if not components_loaded:
        try:
            kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features = load_components()
            components_loaded = True
            print("ML components loaded successfully")
        except Exception as e:
            print(f"Error loading ML components: {e}")
            raise

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

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
        
        # Get recommendations
        if artist_name:
            recommendations = recommend_from_name(song_name, artist_name)
        else:
            recommendations = recommend_from_name(song_name)
        
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
            
            recommendations = manual_selection_fallback(df_pca, df_clean, song_name, artist_name)
            
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

if __name__ == '__main__':
    # Load ML components at startup
    try:
        load_ml_components()
        print("Starting Spotify Recommendation Web App...")
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"Failed to start application: {e}")
        print("Make sure all required model files are present:")
        print("- kmeans_model.pkl")
        print("- pca_transformer.pkl") 
        print("- standard_scaler.pkl")
        print("- minmax_scaler_tempo.pkl")
        print("- df_pca.pkl")
        print("- df_clean.pkl")
        print("- top_features.txt")
