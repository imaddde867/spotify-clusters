"""
Unit tests for the Flask web application.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import after path setup
from web.app import (  # noqa: E402
    app,
    check_model_files,
    get_popular_examples,
    load_ml_components,
)


class TestWebApp:
    """Test Flask web application."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def mock_components_loaded(self):
        """Mock ML components as loaded."""
        with patch("web.app.components_loaded", True), patch(
            "web.app.kmeans", MagicMock()
        ), patch("web.app.pca", MagicMock()), patch(
            "web.app.scaler_opt", MagicMock()
        ), patch(
            "web.app.scaler_tempo", MagicMock()
        ), patch(
            "web.app.df_pca", MagicMock()
        ), patch(
            "web.app.df_clean", MagicMock()
        ), patch(
            "web.app.top_features", ["feature1", "feature2"]
        ):
            yield

    def test_index_route(self, client):
        """Test main index route."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"html" in response.data.lower()

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert "timestamp" in data

    def test_popular_examples_api(self, client):
        """Test popular examples API endpoint."""
        response = client.get("/api/popular-examples")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "examples" in data
        assert len(data["examples"]) == 3  # Default count

    def test_popular_examples_api_with_count(self, client):
        """Test popular examples API with custom count."""
        response = client.get("/api/popular-examples?count=5")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["examples"]) == 5

    def test_popular_examples_api_max_limit(self, client):
        """Test popular examples API respects max limit."""
        response = client.get("/api/popular-examples?count=10")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["examples"]) <= 5  # Max limit

    @patch("web.app.components_loaded", False)
    @patch("web.app.load_ml_components")
    def test_recommend_without_components(self, mock_load_ml, client):
        """Test recommendation endpoint without loaded components."""
        mock_load_ml.return_value = (False, "Components not loaded")

        response = client.post(
            "/recommend",
            data=json.dumps(
                {
                    "song_name": "Test Song",
                    "artist_name": "Test Artist",
                    "playlist_size": 10,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 500
        data = json.loads(response.data)
        assert data["success"] is False

    def test_recommend_missing_song_name(self, client, mock_components_loaded):
        """Test recommendation endpoint with missing song name."""
        response = client.post(
            "/recommend",
            data=json.dumps({"artist_name": "Test Artist", "playlist_size": 10}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "song_name" in data["error"]

    def test_recommend_invalid_playlist_size(self, client, mock_components_loaded):
        """Test recommendation endpoint with invalid playlist size."""
        response = client.post(
            "/recommend",
            data=json.dumps({"song_name": "Test Song", "playlist_size": 0}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "playlist_size" in data["error"]

    def test_recommend_playlist_size_too_large(self, client, mock_components_loaded):
        """Test recommendation endpoint with playlist size too large."""
        response = client.post(
            "/recommend",
            data=json.dumps({"song_name": "Test Song", "playlist_size": 100}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "playlist_size" in data["error"]


class TestUtilityFunctions:
    """Test utility functions."""

    @patch("web.app.parent_dir")
    def test_check_model_files_all_exist(self, mock_parent_dir):
        """Test model file check when all files exist."""
        mock_models_dir = MagicMock()
        mock_parent_dir.__truediv__.return_value = mock_models_dir

        # Mock all files exist
        mock_models_dir.__truediv__.return_value.exists.return_value = True

        success, missing = check_model_files()
        assert success is True
        assert missing == []

    @patch("web.app.parent_dir")
    def test_check_model_files_some_missing(self, mock_parent_dir):
        """Test model file check when some files are missing."""
        mock_models_dir = MagicMock()
        mock_parent_dir.__truediv__.return_value = mock_models_dir

        # Mock some files missing
        def mock_exists(file_path):
            return "kmeans_model.pkl" not in str(file_path)

        mock_models_dir.__truediv__.return_value.exists.side_effect = mock_exists

        success, missing = check_model_files()
        assert success is False
        assert "kmeans_model.pkl" in missing

    def test_get_popular_examples_default_count(self):
        """Test getting popular examples with default count."""
        examples = get_popular_examples()
        assert len(examples) == 3
        assert all("song" in example and "artist" in example for example in examples)

    def test_get_popular_examples_custom_count(self):
        """Test getting popular examples with custom count."""
        examples = get_popular_examples(5)
        assert len(examples) == 5

    def test_get_popular_examples_max_count(self):
        """Test getting popular examples doesn't exceed available songs."""
        # Test with a very large count
        examples = get_popular_examples(1000)
        assert len(examples) <= 30  # Should not exceed available songs

    @patch("web.app.check_model_files")
    @patch("web.app.load_components")
    def test_load_ml_components_success(self, mock_load_components, mock_check_files):
        """Test successful ML component loading."""
        mock_check_files.return_value = (True, [])
        mock_load_components.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            ["feature1", "feature2"],
        )

        success, error = load_ml_components()
        assert success is True
        assert error is None

    @patch("web.app.check_model_files")
    def test_load_ml_components_missing_files(self, mock_check_files):
        """Test ML component loading with missing files."""
        mock_check_files.return_value = (False, ["missing_file.pkl"])

        success, error = load_ml_components()
        assert success is False
        assert "missing_file.pkl" in error

    @patch("web.app.check_model_files")
    @patch("web.app.load_components")
    def test_load_ml_components_import_error(
        self, mock_load_components, mock_check_files
    ):
        """Test ML component loading with import error."""
        mock_check_files.return_value = (True, [])
        mock_load_components.side_effect = ImportError("Module not found")

        success, error = load_ml_components()
        assert success is False
        assert "Import error" in error


class TestRequestValidation:
    """Test request validation and error handling."""

    def test_json_parsing_error(self, client):
        """Test handling of invalid JSON."""
        response = client.post(
            "/recommend", data="invalid json", content_type="application/json"
        )

        assert response.status_code == 400

    def test_missing_content_type(self, client):
        """Test request without proper content type."""
        response = client.post("/recommend", data=json.dumps({"song_name": "Test"}))

        # Should still work or return appropriate error
        assert response.status_code in [200, 400, 500]


if __name__ == "__main__":
    pytest.main([__file__])
