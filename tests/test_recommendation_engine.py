"""
Unit tests for the recommendation engine module.
"""

import json
import sys
import unittest.mock
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from recommendation_engine import (  # noqa: E402
    fix_dataframe_alignment,
    get_random_recommendations,
    load_song_cache,
    save_to_cache,
)


class TestCacheFunctions:
    """Test caching functionality."""

    def test_load_song_cache_empty(self):
        """Test loading cache when file doesn't exist."""
        with patch("recommendation_engine.Path") as mock_path:
            mock_path.return_value.exists.return_value = False
            cache = load_song_cache()
            assert cache == {}

    def test_load_song_cache_with_data(self):
        """Test loading cache with existing data."""
        test_data = {"test_song": {"artist": "test_artist", "features": {}}}
        with patch("recommendation_engine.Path") as mock_path, patch(
            "builtins.open", unittest.mock.mock_open(read_data=json.dumps(test_data))
        ):
            mock_path.return_value.exists.return_value = True
            cache = load_song_cache()
            assert cache == test_data

    def test_save_to_cache(self):
        """Test saving data to cache."""
        test_song_key = "test_song"
        test_song_data = {"artist": "test_artist", "features": {}}

        with patch("recommendation_engine.load_song_cache", return_value={}), patch(
            "builtins.open", unittest.mock.mock_open()
        ), patch("json.dump") as mock_json_dump:
            save_to_cache(test_song_key, test_song_data)
            mock_json_dump.assert_called_once()


class TestDataFrameAlignment:
    """Test dataframe alignment functionality."""

    def test_fix_dataframe_alignment_success(self):
        """Test successful dataframe alignment."""
        # Create test dataframes
        df_pca = pd.DataFrame(
            {"pc1": [1, 2, 3], "pc2": [4, 5, 6]}, index=["track1", "track2", "track3"]
        )
        df_pca.index.name = "track_id"

        df_clean = pd.DataFrame(
            {
                "track_id": ["track1", "track2", "track3", "track4"],
                "track_name": ["Song 1", "Song 2", "Song 3", "Song 4"],
                "artist_name": ["Artist 1", "Artist 2", "Artist 3", "Artist 4"],
            }
        )

        df_pca_aligned, df_clean_aligned = fix_dataframe_alignment(df_pca, df_clean)

        # Check that both dataframes have same indices
        assert set(df_pca_aligned.index) == set(df_clean_aligned.index)
        assert len(df_pca_aligned) == 3  # Only common tracks
        assert len(df_clean_aligned) == 3  # Only common tracks

    def test_fix_dataframe_alignment_no_common_tracks(self):
        """Test dataframe alignment when no common tracks exist."""
        df_pca = pd.DataFrame({"pc1": [1, 2]}, index=["track1", "track2"])
        df_pca.index.name = "track_id"

        df_clean = pd.DataFrame(
            {
                "track_id": ["track3", "track4"],
                "track_name": ["Song 3", "Song 4"],
                "artist_name": ["Artist 3", "Artist 4"],
            }
        )

        with pytest.raises(ValueError, match="No common track IDs found"):
            fix_dataframe_alignment(df_pca, df_clean)


class TestRecommendationFunctions:
    """Test recommendation functionality."""

    def test_get_random_recommendations(self):
        """Test random recommendation generation."""
        df_clean = pd.DataFrame(
            {
                "track_name": ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5"],
                "artist_name": [
                    "Artist 1",
                    "Artist 2",
                    "Artist 3",
                    "Artist 4",
                    "Artist 5",
                ],
                "genre": ["pop", "rock", "jazz", "blues", "country"],
            }
        )

        recommendations = get_random_recommendations(df_clean, n_recommendations=3)

        assert len(recommendations) == 3
        assert all(
            col in recommendations.columns for col in ["track_name", "artist_name"]
        )

    def test_get_random_recommendations_more_than_available(self):
        """Test random recommendations when requesting more than available."""
        df_clean = pd.DataFrame(
            {
                "track_name": ["Song 1", "Song 2"],
                "artist_name": ["Artist 1", "Artist 2"],
            }
        )

        recommendations = get_random_recommendations(df_clean, n_recommendations=5)

        assert len(recommendations) == 2  # Only return what's available


class TestIntegration:
    """Integration tests for recommendation engine."""

    @patch("recommendation_engine.load_components")
    def test_manual_testing_with_mocked_components(self, mock_load_components):
        """Test manual testing function with mocked components."""
        # Mock the loaded components
        mock_kmeans = MagicMock()
        mock_pca = MagicMock()
        mock_scaler_opt = MagicMock()
        mock_scaler_tempo = MagicMock()

        df_pca = pd.DataFrame(
            {"pc1": [1, 2, 3], "pc2": [4, 5, 6]}, index=["track1", "track2", "track3"]
        )
        df_pca.index.name = "track_id"

        df_clean = pd.DataFrame(
            {
                "track_id": ["track1", "track2", "track3"],
                "track_name": ["Song 1", "Song 2", "Song 3"],
                "artist_name": ["Artist 1", "Artist 2", "Artist 3"],
                "genre": ["pop", "rock", "jazz"],
            }
        ).set_index("track_id")

        top_features = ["feature1", "feature2", "feature3"]

        mock_load_components.return_value = (
            mock_kmeans,
            mock_pca,
            mock_scaler_opt,
            mock_scaler_tempo,
            df_pca,
            df_clean,
            top_features,
        )

        from recommendation_engine import manual_testing

        # Mock random.choice to return predictable result
        with patch("recommendation_engine.random.choice", return_value="track1"):
            result = manual_testing()

        assert isinstance(result, pd.DataFrame)
        mock_load_components.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
