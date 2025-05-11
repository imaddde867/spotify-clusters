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

# Load environment variables from .env file
load_dotenv()

# Initialize song features cache
CACHE_PATH = "song_features_cache.json"

def load_song_cache():
    """Load the song features cache from disk"""
    try:
        if Path(CACHE_PATH).exists():
            with open(CACHE_PATH, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading cache: {e}")
        return {}

def save_to_cache(song_key, song_data):
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

def load_components():
    try:
        # Load saved components with explicit error handling
        kmeans = joblib.load('kmeans_model.pkl')
        pca = joblib.load('pca_transformer.pkl')
        scaler_opt = joblib.load('standard_scaler.pkl')
        scaler_tempo = joblib.load('minmax_scaler_tempo.pkl')
        df_pca = pd.read_pickle('df_pca.pkl')
        df_clean = pd.read_pickle('df_clean.pkl')
        
        # Load list of top features
        with open('top_features.txt', 'r') as f:
            top_features = f.read().splitlines()
            
        print("All components loaded successfully.")
        return kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features
    except Exception as e:
        print(f"Error loading components: {e}")
        raise

def authenticate_spotify():
    """
    Authenticate with Spotify API with proper error handling
    """
    try:
        # First try to get credentials from environment variables
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        # If not in environment, use hardcoded credentials as backup
        # Note: This is not best practice for security, but for this case helps resolve immediate issues
        if not client_id or not client_secret:
            print("Warning: Using backup credentials method")
            client_id = "d6197acc06764f4797a5537c2f5a2b16"
            client_secret = "32044bbc741c43f78eac19e8b12a03cf"
        
        # Check if credentials exist
        if not client_id or not client_secret:
            raise ValueError("Missing Spotify API credentials. Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables.")
        
        # Create client
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=20)
        
        # Test the connection with a gentle request
        try:
            sp.album('4aawyAB9vmqN3uQ7FjRGTy')  # Use a specific album ID for testing (a popular album)
            return sp
        except Exception as e:
            print(f"Connection test failed: {e}")
            raise
            
    except ValueError as e:
        print(f"Authentication Error: {e}")
        raise
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")
        print("Possible causes: Invalid credentials, expired token, or API rate limiting")
        raise
    except Exception as e:
        print(f"Unexpected error during authentication: {e}")
        raise

def find_song(sp, song_name, artist_name=None):
    """
    Search for the song data on Spotify based on its name to get its features
    Parameters:
        sp (Spotify object): Authenticated Spotify connection
        song_name (str): The name of the song to search for.
        artist_name (str, optional): The artist name to refine search.

    Returns:
        song_data (dict): A dictionary containing the song data.
    """
    try:
        # Check cache first
        cache_key = f"{song_name.lower()}|{artist_name.lower() if artist_name else ''}"
        if cache_key in song_cache:
            print(f"Found song in cache: {song_name}")
            return song_cache[cache_key]
        
        # Build search query
        query = f'track:{song_name}'
        if artist_name:
            query += f' artist:{artist_name}'
        
        # Retry logic with exponential backoff for API rate limiting
        max_retries = 4  # Increased retries
        retry_delay = 2  # Start with longer delay
        
        for attempt in range(max_retries):
            try:
                results = sp.search(q=query, type='track', limit=1)
                break  # If successful, exit the retry loop
            except spotipy.exceptions.SpotifyException as e:
                if attempt < max_retries - 1:
                    print(f"API request failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise e  # Re-raise the exception if all retries failed
        
        # Process search results
        if not results['tracks']['items']:
            print(f"No song found for: {song_name}")
            if artist_name:
                # Retry without artist name if no results
                print(f"Retrying search without artist name constraint...")
                return find_song(sp, song_name)
            return None
            
        track = results['tracks']['items'][0]
        track_id = track['id']
        
        # Short pause to avoid rate limiting
        time.sleep(1)
        
        # Get audio features with retry logic
        for attempt in range(max_retries):
            try:
                audio_features = sp.audio_features(track_id)
                break
            except spotipy.exceptions.SpotifyException as e:
                if attempt < max_retries - 1:
                    print(f"API request failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    # If we keep getting API errors, try a different approach - use dataset
                    print("Spotify API rate limiting detected. Falling back to manual selection.")
                    return None
        
        if not audio_features or not audio_features[0]:
            print(f"No audio features found for song: {song_name}")
            return None
            
        # Get the first item from the list
        audio_features = audio_features[0]
        
        # Add non-audio features to the audio features
        audio_features['name'] = track['name']
        audio_features['artist'] = track['artists'][0]['name']
        audio_features['album'] = track['album']['name']
        audio_features['release_date'] = track['album']['release_date']
        
        # Create a dictionary with only the raw features we need
        raw_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 
                       'speechiness', 'acousticness', 'instrumentalness', 
                       'liveness', 'valence', 'tempo']
        
        song_data = {feature: audio_features[feature] for feature in raw_features}
        song_data['name'] = audio_features['name']
        song_data['artist'] = audio_features['artist']
        
        # Save to cache for future use
        save_to_cache(cache_key, song_data)
        
        return song_data
    
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")
        return None
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

        # Extract features that were used in the model
        song_df = song_data[top_features]

        # Apply StandardScaler
        song_scaled = scaler_opt.transform(song_df)
        song_scaled_df = pd.DataFrame(song_scaled, columns=song_df.columns)

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
    Find similar songs within the same cluster
    """
    try:
        # Get songs in the same cluster
        cluster_songs = df_pca[df_pca['cluster'] == cluster].drop('cluster', axis=1)
        
        if len(cluster_songs) < n_recommendations:
            print(f"Warning: Only {len(cluster_songs)} songs found in cluster {cluster}.")
            n_recommendations = len(cluster_songs)
        
        # Calculate distances to all songs in the cluster
        from sklearn.metrics.pairwise import euclidean_distances
        distances = euclidean_distances(song_pca_features, cluster_songs)[0]
        
        # Get the indices of the most similar songs
        similar_indices = np.argsort(distances)[:n_recommendations]
        similar_songs_ids = cluster_songs.iloc[similar_indices].index.tolist()
        
        # Get details of the recommended songs
        recommendations = df_clean.loc[similar_songs_ids]
        
        return recommendations[['track_name', 'artist_name', 'genre', 'popularity']]
    
    except Exception as e:
        print(f"Error finding similar songs: {e}")
        return pd.DataFrame()

def recommend_songs_from_track_id(track_id, df_pca, df_clean, n_recommendations=5):
    """
    Recommend songs based on a track ID that's already in our database
    """
    try:
        if track_id not in df_pca.index:
            print(f"Track ID {track_id} not found in PCA data.")
            return pd.DataFrame({
                'track_name': ['Track ID not found in database'],
                'artist_name': ['Try another song'],
                'genre': [''],
                'popularity': [0]
            })
            
        cluster = df_pca.loc[track_id, 'cluster']
        similar_songs = df_pca[df_pca['cluster'] == cluster].drop('cluster', axis=1)
        
        if len(similar_songs) <= 1:
            print("Not enough songs in the same cluster.")
            return pd.DataFrame({
                'track_name': ['Not enough similar songs found'],
                'artist_name': ['Try another song'],
                'genre': [''],
                'popularity': [0]
            })
            
        # Calculate cosine similarity
        from sklearn.metrics.pairwise import cosine_similarity
        track_features = similar_songs.loc[track_id].values.reshape(1, -1)
        similarities = cosine_similarity(track_features, similar_songs)[0]
        
        # Get top similar songs, ensuring they're in df_clean
        sorted_indices = np.argsort(similarities)[::-1]
        similar_indices = []
        for idx in sorted_indices[1:]:  # Skip the first one which is the song itself
            candidate_id = similar_songs.index[idx]
            if candidate_id in df_clean.index and len(similar_indices) < n_recommendations:
                similar_indices.append(candidate_id)
        
        if not similar_indices:
            print("Could not find similar songs in clean data.")
            return pd.DataFrame({
                'track_name': ['No similar songs found in database'],
                'artist_name': ['Try another song'],
                'genre': [''],
                'popularity': [0]
            })
            
        recommendations = df_clean.loc[similar_indices]
        
        # Ensure we have all required columns
        required_cols = ['track_name', 'artist_name', 'genre', 'popularity']
        for col in required_cols:
            if col not in recommendations.columns:
                if col == 'track_name':
                    recommendations[col] = ['Unknown track'] * len(recommendations)
                elif col == 'artist_name':
                    recommendations[col] = ['Unknown artist'] * len(recommendations)
                elif col == 'genre':
                    recommendations[col] = [''] * len(recommendations)
                elif col == 'popularity':
                    recommendations[col] = [0] * len(recommendations)
        
        return recommendations[required_cols]
    
    except Exception as e:
        print(f"Error recommending songs: {e}")
        return pd.DataFrame({
            'track_name': ['Error finding recommendations'],
            'artist_name': ['Try another song'],
            'genre': [''],
            'popularity': [0]
        })

def recommend_from_name(song_name, artist_name=None):
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
                return manual_selection_fallback(df_pca, df_clean, song_name, artist_name)
                
            print(f"Found: {song_data['name']} by {song_data['artist']}")
            
            # Preprocess song
            pca_features = preprocess_song(song_data, scaler_tempo, scaler_opt, pca, top_features)
            
            # Predict cluster
            cluster = predict_cluster(pca_features, kmeans)
            print(f"Song belongs to cluster: {cluster}")
            
            # Find similar songs
            recommendations = find_similar_songs(pca_features, cluster, df_pca, df_clean)
            
            return recommendations
            
        except Exception as api_error:
            print(f"Spotify API access failed: {api_error}")
            print("Falling back to manual selection...")
            return manual_selection_fallback(df_pca, df_clean, song_name, artist_name)
    
    except Exception as e:
        print(f"Error in recommendation process: {e}")
        return f"Error: {str(e)}"

def manual_selection_fallback(df_pca, df_clean, song_name=None, artist_name=None):
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
                    return recommend_songs_from_track_id(track_id, df_pca, df_clean)
                else:
                    print(f"Track ID {track_id} not found in PCA data. Using random selection instead.")
        
        # If no match or no song name provided, use random selection
        print("Selecting a random track from our dataset...")
        
        # Select a track that exists in both dataframes to avoid key errors
        common_indices = set(df_pca.index).intersection(set(df_clean.index))
        if not common_indices:
            print("No common tracks found between dataframes. Using ultimate fallback...")
            return pd.DataFrame({
                'track_name': ['Sorry, could not find recommendations'],
                'artist_name': ['Try another song'],
                'genre': [''],
                'popularity': [0]
            })
            
        # Select a random track from common indices
        import random
        sample_track_id = random.choice(list(common_indices))
        
        # Get information about the selected song
        song_info = df_clean.loc[sample_track_id]
        print(f"Selected random track: {song_info['track_name']} by {song_info['artist_name']}")
        if 'genre' in song_info:
            print(f"Genre: {song_info['genre']}")
        
        # Get recommendations based on this track
        try:
            return recommend_songs_from_track_id(sample_track_id, df_pca, df_clean)
        except Exception as rec_error:
            print(f"Error getting recommendations: {rec_error}")
            return pd.DataFrame({
                'track_name': ['Sorry, could not find recommendations'],
                'artist_name': ['Try another song'],
                'genre': [''],
                'popularity': [0]
            })
        
    except Exception as e:
        print(f"Error in manual selection fallback: {e}")
        # Return a dataframe with an error message instead of trying more fallbacks
        return pd.DataFrame({
            'track_name': ['Sorry, could not find recommendations'],
            'artist_name': ['Try another song'],
            'genre': [''],
            'popularity': [0]
        })

# Manual Testing Function (fallback when Spotify API is unavailable)
def manual_testing(song_name=None):
    """
    Test recommendation functionality using a random song from our dataset
    (This doesn't require Spotify API)
    """
    try:
        # Load components
        kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features = load_components()
        
        # Select a random song from dataset, ensuring it exists in both dataframes
        import random
        common_indices = set(df_pca.index).intersection(set(df_clean.index))
        if not common_indices:
            return pd.DataFrame({
                'track_name': ['No common tracks found in database'],
                'artist_name': ['Please check data integrity'],
                'genre': [''],
                'popularity': [0]
            })
            
        sample_track_id = random.choice(list(common_indices))
        
        # Get information about the selected song
        song_info = df_clean.loc[sample_track_id]
        print(f"Selected random track: {song_info['track_name']} by {song_info['artist_name']}")
        if 'genre' in song_info:
            print(f"Genre: {song_info['genre']}")
        print(f"Track ID: {sample_track_id}")
        
        # Get recommendations
        print("\nRecommendations:")
        try:
            recommendations = recommend_songs_from_track_id(sample_track_id, df_pca, df_clean)
            return recommendations
        except Exception as rec_error:
            print(f"Error getting recommendations: {rec_error}")
            return pd.DataFrame({
                'track_name': ['Error finding recommendations'],
                'artist_name': ['Try again'],
                'genre': [''],
                'popularity': [0]
            })
        
    except Exception as e:
        print(f"Error in manual testing: {e}")
        return pd.DataFrame({
            'track_name': ['Error in recommendation system'],
            'artist_name': ['Please check logs'],
            'genre': [''],
            'popularity': [0]
        })

if __name__ == "__main__":
    print("\n===== Spotify Music Recommendation System =====\n")
    
    try:
        # Try to authenticate with Spotify
        sp = authenticate_spotify()
        print("Successfully connected to Spotify API")
        
        # If successful, use the full recommendation system
        song_name = input("Enter a song name: ")
        artist_name = input("Enter artist name (optional, press Enter to skip): ")
        if not artist_name:
            artist_name = None
            
        recommendations = recommend_from_name(song_name, artist_name)
        print("\nRecommended songs:")
        print(recommendations)
        
    except Exception as e:
        print(f"\nCould not connect to Spotify API: {e}")
        print("\nFalling back to manual testing mode using existing dataset...")
        
        # Still allow user to input song details for potential dataset matching
        song_name = input("Enter a song name to search in our dataset (or press Enter for random selection): ")
        if song_name:
            artist_name = input("Enter artist name (optional): ")
            if not artist_name:
                artist_name = None
                
            # Load components for the manual fallback
            kmeans, pca, scaler_opt, scaler_tempo, df_pca, df_clean, top_features = load_components()
            recommendations = manual_selection_fallback(df_pca, df_clean, song_name, artist_name)
        else:
            recommendations = manual_testing()
            
        print("\nRecommended songs:")
        print(recommendations)