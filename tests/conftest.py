"""
Test configuration and fixtures.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest


@pytest.fixture
def app():
    """Create Flask app for testing."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    
    from web.app import app
    app.config["TESTING"] = True
    return app


@pytest.fixture
def temp_cache_file():
    """Create a temporary cache file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def sample_df_clean():
    """Create a sample clean dataframe for testing."""
    return pd.DataFrame({
        "track_name": ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5"],
        "artist_name": ["Artist 1", "Artist 2", "Artist 3", "Artist 4", "Artist 5"],
        "genre": ["pop", "rock", "jazz", "blues", "country"],
        "danceability": [0.5, 0.7, 0.3, 0.6, 0.4],
        "energy": [0.8, 0.9, 0.4, 0.7, 0.5],
        "valence": [0.6, 0.8, 0.2, 0.5, 0.3],
    }, index=["track1", "track2", "track3", "track4", "track5"])


@pytest.fixture
def sample_df_pca():
    """Create a sample PCA dataframe for testing."""
    df = pd.DataFrame({
        "pc1": [1.0, 2.0, 3.0, 4.0, 5.0],
        "pc2": [1.1, 2.1, 3.1, 4.1, 5.1],
        "pc3": [1.2, 2.2, 3.2, 4.2, 5.2],
    }, index=["track1", "track2", "track3", "track4", "track5"])
    df.index.name = "track_id"
    return df


@pytest.fixture
def mock_ml_components():
    """Create mock ML components for testing."""
    mock_kmeans = MagicMock()
    mock_kmeans.predict.return_value = [0]
    
    mock_pca = MagicMock()
    mock_pca.transform.return_value = [[1.0, 2.0, 3.0]]
    
    mock_scaler_opt = MagicMock()
    mock_scaler_opt.transform.return_value = [[0.5, 0.6, 0.7]]
    
    mock_scaler_tempo = MagicMock()
    mock_scaler_tempo.transform.return_value = [[120.0]]
    
    top_features = ["danceability", "energy", "valence", "acousticness", "instrumentalness"]
    
    return mock_kmeans, mock_pca, mock_scaler_opt, mock_scaler_tempo, top_features


@pytest.fixture
def mock_spotify_api():
    """Create a mock Spotify API client."""
    mock_sp = MagicMock()
    
    # Mock search results
    mock_sp.search.return_value = {
        "tracks": {
            "items": [{
                "id": "test_track_id",
                "name": "Test Song",
                "artists": [{"name": "Test Artist"}],
                "album": {"name": "Test Album"},
                "external_urls": {"spotify": "https://open.spotify.com/track/test_track_id"}
            }]
        }
    }
    
    # Mock audio features
    mock_sp.audio_features.return_value = [{
        "danceability": 0.5,
        "energy": 0.8,
        "valence": 0.6,
        "acousticness": 0.3,
        "instrumentalness": 0.1,
        "liveness": 0.2,
        "speechiness": 0.1,
        "tempo": 120.0,
        "loudness": -10.0,
        "duration_ms": 240000
    }]
    
    return mock_sp


@pytest.fixture(scope="session")
def test_models_dir():
    """Create a temporary directory with mock model files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        models_dir = Path(temp_dir) / "models"
        models_dir.mkdir()
        
        # Create mock model files
        model_files = [
            "kmeans_model.pkl",
            "pca_transformer.pkl", 
            "standard_scaler.pkl",
            "minmax_scaler_tempo.pkl",
            "df_pca.pkl",
            "df_clean.pkl",
            "top_features.txt"
        ]
        
        for file_name in model_files:
            (models_dir / file_name).touch()
        
        # Create actual content for top_features.txt
        with open(models_dir / "top_features.txt", "w") as f:
            f.write("danceability\nenergy\nvalence\nacousticness\ninstrumentalness")
        
        yield models_dir


@pytest.fixture
def mock_environment_variables():
    """Mock environment variables for testing."""
    env_vars = {
        "SPOTIPY_CLIENT_ID": "test_client_id",
        "SPOTIPY_CLIENT_SECRET": "test_client_secret",
        "FLASK_SECRET_KEY": "test_secret_key"
    }
    
    with pytest.MonkeyPatch().context() as m:
        for key, value in env_vars.items():
            m.setenv(key, value)
        yield env_vars