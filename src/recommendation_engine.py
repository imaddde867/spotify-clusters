import pandas as pd
import os
import joblib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import time
import json
from pathlib import Path
from dotenv import load_dotenv
import random
import warnings
from typing import Dict, List, Optional, Tuple, Any, Union

# Suppress mathematical warnings globally for cleaner output
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=UserWarning)
np.seterr(all='ignore')

# Load environment variables from .env file
load_dotenv()

# Constants
CACHE_PATH = "song_features_cache.json"
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1
API_RATE_LIMIT_PAUSE = 0.5

def load_song_cache() -> Dict[str, Dict[str, Any]]:
    """Load the song features cache from disk"""
    try:
        if Path(CACHE_PATH).exists():
            with open(CACHE_PATH, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading cache: {e}")
        return {}

def save_to_cache(song_key: str, song_data: Dict[str, Any]) -> None:
    """Save song data to cache"""
    try:
        cache = load_song_cache()
        cache[song_key] = song_data
        with open(CACHE_PATH, 'w') as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"Error saving to cache: {e}")

# Load song cache
song_cache = load_song_cache()

def load_components() -> Tuple[Any, Any, Any, Any, pd.DataFrame, pd.DataFrame, List[str]]:
    """Load all required ML components and data"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(script_dir, 'models')

        # Load saved components
        kmeans = joblib.load(os.path.join(models_dir, 'kmeans_model.pkl'))
        pca = joblib.load(os.path.join(models_dir, 'pca_transformer.pkl'))
        scaler_opt = joblib.load(os.path.join(models_dir, 'standard_scaler.pkl'))
        scaler_tempo = joblib.load(os.path.join(models_dir, 'minmax_scaler_tempo.pkl'))
        df_pca = pd.read_pickle(os.path.join(models_dir, 'df_pca.pkl'))
        df_clean = pd.read_pickle(os.path.join(models_dir, 'df_clean.pkl'))

        # Load list of top features
        with open(os.path.join(models_dir, 'top_features.txt'), 'r') as f:
            top_features = f.read().splitlines()

        print("All components loaded successfully.")

        # Fix data alignment issue
        df_pca, df_clean = fix_dataframe_alignment(df_pca, df_clean)

        return kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features
    except Exception as e:
        print(f"Error loading components: {e}")
        raise

def fix_dataframe_alignment(df_pca: pd.DataFrame, df_clean: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fix the data alignment issue between df_pca and df_clean"""
    try:
        print("Fixing dataframe alignment...")

        # Set track_id as index for both dataframes
        if df_clean.index.name != 'track_id' and 'track_id' in df_clean.columns:
            df_clean = df_clean.set_index('track_id')
            df_clean.index.name = 'track_id'

        if df_pca.index.name != 'track_id':
            df_pca.index.name = 'track_id'

        # Filter to common tracks
        common_track_ids = set(df_pca.index).intersection(set(df_clean.index))
        if not common_track_ids:
            raise ValueError("No common track IDs found between dataframes!")

        df_pca = df_pca.loc[list(common_track_ids)]
        df_clean = df_clean.loc[list(common_track_ids)]
        print(f"Filtered dataframes to {len(common_track_ids)} common tracks")

        return df_pca, df_clean

    except Exception as e:
        print(f"Error fixing dataframe alignment: {e}")
        raise

def authenticate_spotify() -> spotipy.Spotify:
    """Authenticate with Spotify API"""
    try:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise ValueError("Missing Spotify API credentials")

        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=30, retries=5)
        
        # Test connection
        sp.album('4aawyAB9vmqN3uQ7FjRGTy')
        print("Spotify API connection successful")
        return sp
            
    except Exception as e:
        print(f"Authentication Error: {e}")
        raise

def find_song(sp: spotipy.Spotify, song_name: str, artist_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Search for song data on Spotify"""
    try:
        # Check cache
        cache_key = f"{song_name.lower()}|{artist_name.lower() if artist_name else ''}"
        if cache_key in song_cache:
            print(f"Found song in cache: {song_name}")
            return song_cache[cache_key]
        
        # Build search query
        query = f'track:{song_name}'
        if artist_name:
            query += f' artist:{artist_name}'
        
        # Search with retry logic
        retry_delay = INITIAL_RETRY_DELAY
        for attempt in range(MAX_RETRIES):
            try:
                results = sp.search(q=query, type='track', limit=1)
                break
            except spotipy.exceptions.SpotifyException as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"API request failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Search failed after {MAX_RETRIES} attempts: {e}")
                    return None
        
        if not results['tracks']['items']:
            if artist_name:
                return find_song(sp, song_name)
            return None
            
        track = results['tracks']['items'][0]
        track_id = track['id']
        
        time.sleep(API_RATE_LIMIT_PAUSE)
        
        # Get audio features with retry logic
        retry_delay = INITIAL_RETRY_DELAY
        for attempt in range(MAX_RETRIES):
            try:
                audio_features = sp.audio_features(track_id)
                break
            except spotipy.exceptions.SpotifyException as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"API request failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Failed to get audio features after {MAX_RETRIES} attempts.")
                    return None
        
        if not audio_features or not audio_features[0]:
            return None
            
        audio_features = audio_features[0]
        
        # Add metadata
        audio_features.update({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date']
        })
        
        # Cache the result
        save_to_cache(cache_key, audio_features)
        
        return audio_features

    except Exception as e:
        print(f"Error finding song: {e}")
        return None

def preprocess_song(song_data, scaler_tempo, scaler_opt, pca, top_features):
    '''
    Preprocess new song data to match the format of the preprocessed dataset
    '''
    try:
        # Convert the song_data to a pandas dataframe if necessary
        if not isinstance(song_data, pd.DataFrame):
            song_data = pd.DataFrame(song_data, index=[0])

        # Ensure all necessary columns are present
        raw_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 
                       'speechiness', 'acousticness', 'instrumentalness', 
                       'liveness', 'valence', 'tempo']
        
        for feature in raw_features:
            if feature not in song_data.columns:
                raise ValueError(f"Missing required feature: {feature}")

        # Create new features
        song_data['energy_to_acousticness_ratio'] = song_data['energy'] / (song_data['acousticness'] + 0.01)
        song_data['energy_dynamics'] = song_data['energy']
        song_data['dance_rhythm'] = 0.6 * song_data['danceability'] + 0.4 * song_data['tempo']
        song_data['emotional_content'] = song_data['valence']
        song_data['vocal_presence'] = song_data['speechiness'] - 0.5 * song_data['instrumentalness']
        song_data['performance_style'] = song_data['liveness']

        # Scale tempo if it's not already scaled
        if song_data['tempo'].max() > 1.0:
            song_data['tempo'] = scaler_tempo.transform(song_data[['tempo']])

        # Extract features that were used in the model, handle missing features
        feature_df = pd.DataFrame()
        for feature in top_features:
            if feature in song_data.columns:
                feature_df[feature] = song_data[feature]
            else:
                print(f"Warning: Feature '{feature}' not found, using default value 0")
                feature_df[feature] = 0
        
        # Apply StandardScaler
        song_scaled = scaler_opt.transform(feature_df)
        song_scaled_df = pd.DataFrame(song_scaled, columns=feature_df.columns)

        # Apply PCA
        pca_features = pca.transform(song_scaled_df)
        pca_features_df = pd.DataFrame(pca_features, columns=[f'PC{i+1}' for i in range(pca.n_components_)])

        return pca_features_df
    
    except Exception as e:
        print(f"Error preprocessing song: {e}")
        raise

def predict_cluster(pca_features, kmeans):
    """
    Predict the cluster for a song based on its PCA features
    """
    try:
        cluster = kmeans.predict(pca_features)[0]
        return cluster
    except Exception as e:
        print(f"Error predicting cluster: {e}")
        raise

def find_similar_songs(song_pca_features, cluster, df_pca, df_clean, n_recommendations=5):
    """
    Find similar songs within the same cluster using improved data alignment
    """
    try:
        # Get songs in the same cluster
        cluster_songs = df_pca[df_pca['cluster'] == cluster].drop('cluster', axis=1)

        if len(cluster_songs) < n_recommendations:
            print(f"Warning: Only {len(cluster_songs)} songs found in cluster {cluster}.")
            n_recommendations = len(cluster_songs)

        if len(cluster_songs) == 0:
            print(f"No songs found in cluster {cluster}. Using random selection instead.")
            return get_random_recommendations(df_clean, n_recommendations)

        # Calculate distances to all songs in the cluster with error handling
        from sklearn.metrics.pairwise import euclidean_distances
        import warnings
        import numpy as np

        # Suppress all mathematical warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            np.seterr(all='ignore')

            try:
                distances = euclidean_distances(song_pca_features, cluster_songs)[0]
                # Handle any NaN or infinite values
                distances = np.nan_to_num(distances, nan=1.0, posinf=1.0, neginf=0.0)
            except Exception as e:
                print(f"Distance calculation failed, using fallback: {e}")
                # Fallback to random distances
                distances = np.random.random(len(cluster_songs))
            finally:
                # Reset numpy error handling
                np.seterr(all='warn')

        # Get the indices of the most similar songs
        similar_indices = np.argsort(distances)[:n_recommendations]
        similar_track_ids = cluster_songs.iloc[similar_indices].index.tolist()

        # Get details of the recommended songs using track_id index
        valid_track_ids = [track_id for track_id in similar_track_ids if track_id in df_clean.index]

        if not valid_track_ids:
            print("No valid track IDs found in df_clean. Using random selection.")
            return get_random_recommendations(df_clean, n_recommendations)

        recommendations = df_clean.loc[valid_track_ids]

        # Ensure we have all required columns with proper fallbacks
        required_cols = ['track_name', 'artist_name', 'genre', 'popularity']
        recommendations_clean = pd.DataFrame(index=recommendations.index)

        for col in required_cols:
            if col in recommendations.columns:
                recommendations_clean[col] = recommendations[col]
            else:
                if col == 'track_name':
                    recommendations_clean[col] = 'Unknown Track'
                elif col == 'artist_name':
                    recommendations_clean[col] = 'Unknown Artist'
                elif col == 'genre':
                    recommendations_clean[col] = ''
                elif col == 'popularity':
                    recommendations_clean[col] = 0

        return recommendations_clean

    except Exception as e:
        print(f"Error finding similar songs: {e}")
        return get_random_recommendations(df_clean, n_recommendations)

def get_random_recommendations(df_clean, n_recommendations=5):
    """Helper function to get random recommendations when other methods fail"""
    try:
        if len(df_clean) <= n_recommendations:
            sample_tracks = df_clean.copy()
        else:
            sample_tracks = df_clean.sample(n=n_recommendations)

        # Ensure we have all required columns with proper fallbacks
        required_cols = ['track_name', 'artist_name', 'genre', 'popularity']
        recommendations_clean = pd.DataFrame(index=sample_tracks.index)

        for col in required_cols:
            if col in sample_tracks.columns:
                recommendations_clean[col] = sample_tracks[col]
            else:
                if col == 'track_name':
                    recommendations_clean[col] = 'Random Track'
                elif col == 'artist_name':
                    recommendations_clean[col] = 'Random Artist'
                elif col == 'genre':
                    recommendations_clean[col] = ''
                elif col == 'popularity':
                    recommendations_clean[col] = 0

        return recommendations_clean
    except Exception as e:
        print(f"Error getting random recommendations: {e}")
        # Return a dataframe with an error message
        return pd.DataFrame({
            'track_name': ['Error finding recommendations'] * n_recommendations,
            'artist_name': ['Try another song'] * n_recommendations,
            'genre': [''] * n_recommendations,
            'popularity': [0] * n_recommendations
        })

def recommend_songs_from_track_id(track_id, df_pca, df_clean, n_recommendations=5):
    """
    Recommend songs based on a track ID that's already in our database
    """
    try:
        if track_id not in df_pca.index:
            print(f"Track ID {track_id} not found in PCA data.")
            return get_random_recommendations(df_clean, n_recommendations)
            
        cluster = df_pca.loc[track_id, 'cluster']
        similar_songs = df_pca[df_pca['cluster'] == cluster].drop('cluster', axis=1)
        
        if len(similar_songs) <= 1:
            print("Not enough songs in the same cluster.")
            return get_random_recommendations(df_clean, n_recommendations)
            
        # Calculate cosine similarity with comprehensive error handling
        from sklearn.metrics.pairwise import cosine_similarity
        import warnings
        import numpy as np

        track_features = similar_songs.loc[track_id].values.reshape(1, -1)

        # Suppress all mathematical warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Also suppress numpy warnings specifically
            np.seterr(all='ignore')

            try:
                similarities = cosine_similarity(track_features, similar_songs)[0]
                # Handle any NaN or infinite values
                similarities = np.nan_to_num(similarities, nan=0.0, posinf=1.0, neginf=0.0)
            except Exception as e:
                print(f"Similarity calculation failed, using fallback: {e}")
                # Fallback to simple distance calculation
                similarities = np.ones(len(similar_songs)) * 0.5
            finally:
                # Reset numpy error handling
                np.seterr(all='warn')
        
        # Get top similar songs, ensuring they're in df_clean
        sorted_indices = np.argsort(similarities)[::-1]
        similar_track_ids = []
        for idx in sorted_indices[1:]:  # Skip the first one which is the song itself
            candidate_track_id = similar_songs.index[idx]
            if candidate_track_id in df_clean.index and len(similar_track_ids) < n_recommendations:
                similar_track_ids.append(candidate_track_id)

        if not similar_track_ids:
            print("Could not find similar songs in clean data.")
            return get_random_recommendations(df_clean, n_recommendations)

        recommendations = df_clean.loc[similar_track_ids]

        # Ensure we have all required columns with proper fallbacks
        required_cols = ['track_name', 'artist_name', 'genre', 'popularity']
        recommendations_clean = pd.DataFrame(index=recommendations.index)

        for col in required_cols:
            if col in recommendations.columns:
                recommendations_clean[col] = recommendations[col]
            else:
                if col == 'track_name':
                    recommendations_clean[col] = 'Unknown Track'
                elif col == 'artist_name':
                    recommendations_clean[col] = 'Unknown Artist'
                elif col == 'genre':
                    recommendations_clean[col] = ''
                elif col == 'popularity':
                    recommendations_clean[col] = 0

        return recommendations_clean
    
    except Exception as e:
        print(f"Error recommending songs: {e}")
        return get_random_recommendations(df_clean, n_recommendations)

def recommend_from_name(song_name, artist_name=None, n_recommendations=5):
    """
    Main function to recommend songs based on a song name
    """
    try:
        # Load components
        kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features = load_components()
        
        # Authenticate with Spotify
        try:
            sp = authenticate_spotify()
            
            # Find song on Spotify
            print(f"Searching for: {song_name}")
            if artist_name:
                print(f"By artist: {artist_name}")
                
            song_data = find_song(sp, song_name, artist_name)
            
            if song_data is None:
                print("Could not find song data. Falling back to manual selection...")
                return manual_selection_fallback(df_pca, df_clean, song_name, artist_name, n_recommendations)
                
            print(f"Found: {song_data['name']} by {song_data['artist']}")
            
            # Preprocess song
            pca_features = preprocess_song(song_data, scaler_tempo, scaler_opt, pca, top_features)
            
            # Predict cluster
            cluster = predict_cluster(pca_features, kmeans)
            print(f"Song belongs to cluster: {cluster}")
            
            # Find similar songs
            recommendations = find_similar_songs(pca_features, cluster, df_pca, df_clean, n_recommendations)

            return recommendations
            
        except Exception as api_error:
            print(f"Spotify API access failed: {api_error}")
            print("Falling back to manual selection...")
            return manual_selection_fallback(df_pca, df_clean, song_name, artist_name, n_recommendations)
    
    except Exception as e:
        print(f"Error in recommendation process: {e}")
        # Ensure we return a DataFrame rather than an error string
        return pd.DataFrame({
            'track_name': ['Error in recommendation system'],
            'artist_name': ['Try another song'],
            'genre': [''],
            'popularity': [0]
        })

def manual_selection_fallback(df_pca, df_clean, song_name=None, artist_name=None, n_recommendations=5):
    """
    Fallback mechanism when Spotify API fails -
    tries to find a similar song in our existing dataset
    """
    try:
        # Try to find a similar song in our dataset based on name/artist
        if song_name:
            print(f"Looking for similar songs to '{song_name}' in our dataset...")
            
            # Case-insensitive partial matching
            song_matches = df_clean[df_clean['track_name'].str.lower().str.contains(song_name.lower(), na=False)]
            
            if artist_name and len(song_matches) > 1:
                # Further filter by artist if provided
                artist_matches = song_matches[song_matches['artist_name'].str.lower().str.contains(artist_name.lower(), na=False)]
                if not artist_matches.empty:
                    song_matches = artist_matches
            
            if not song_matches.empty:
                # Use the first match
                matched_track = song_matches.iloc[0]
                track_id = matched_track.name  # Index is the track_id
                
                print(f"Found similar track in dataset: {matched_track['track_name']} by {matched_track['artist_name']}")
                
                # Verify track_id is in df_pca before recommending
                if track_id in df_pca.index:
                    return recommend_songs_from_track_id(track_id, df_pca, df_clean, n_recommendations)
                else:
                    print(f"Track ID {track_id} not found in PCA data. Using random selection instead.")
        
        # If no match or no song name provided, use random selection
        print("Selecting a random track from our dataset...")
        
        # Select a track that exists in both dataframes to avoid key errors
        common_indices = set(df_pca.index).intersection(set(df_clean.index))
        if not common_indices:
            print("No common tracks found between dataframes. Using ultimate fallback...")
            return get_random_recommendations(df_clean, n_recommendations)
            
        # Select a random track from common indices
        sample_track_id = random.choice(list(common_indices))
        
        # Get information about the selected song
        song_info = df_clean.loc[sample_track_id]
        print(f"Selected random track: {song_info['track_name']} by {song_info['artist_name']}")
        if 'genre' in song_info:
            print(f"Genre: {song_info['genre']}")
        
        # Get recommendations based on this track
        return recommend_songs_from_track_id(sample_track_id, df_pca, df_clean, n_recommendations)
        
    except Exception as e:
        print(f"Error in manual selection fallback: {e}")
        # Return recommendations using only df_clean
        return get_random_recommendations(df_clean, n_recommendations)

# Manual Testing Function (fallback when Spotify API is unavailable)
def manual_testing(song_name=None):
    """
    Test recommendation functionality using a random song from our dataset
    (This doesn't require Spotify API)
    """
    try:
        # Load components
        _, _, _, _, df_pca, df_clean, _ = load_components()
        
        # Select a random song from dataset, ensuring it exists in both dataframes
        common_indices = set(df_pca.index).intersection(set(df_clean.index))
        if not common_indices:
            return get_random_recommendations(df_clean)
            
        sample_track_id = random.choice(list(common_indices))
        
        # Get information about the selected song
        song_info = df_clean.loc[sample_track_id]
        print(f"Selected random track: {song_info['track_name']} by {song_info['artist_name']}")
        if 'genre' in song_info:
            print(f"Genre: {song_info['genre']}")
        print(f"Track ID: {sample_track_id}")
        
        # Get recommendations
        print("\nRecommendations:")
        return recommend_songs_from_track_id(sample_track_id, df_pca, df_clean)
        
    except Exception as e:
        print(f"Error in manual testing: {e}")
        return get_random_recommendations(df_clean)
