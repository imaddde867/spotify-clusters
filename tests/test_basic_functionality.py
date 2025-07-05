"""
Basic unit tests for the Flask web application.
"""

import json
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import after path setup
from web.app import get_popular_examples  # noqa: E402


class TestBasicFunctionality:
    """Test basic functionality without complex mocking."""

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

    def test_get_popular_examples_structure(self):
        """Test the structure of popular examples."""
        examples = get_popular_examples(3)
        for example in examples:
            assert "song" in example
            assert "artist" in example
            assert isinstance(example["song"], str)
            assert isinstance(example["artist"], str)
            assert len(example["song"]) > 0
            assert len(example["artist"]) > 0


class TestWebAppRoutes:
    """Test Flask web application routes."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        from web.app import app

        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_index_route_exists(self, client):
        """Test that main index route exists and returns HTML."""
        response = client.get("/")
        assert response.status_code == 200
        # Should return HTML content
        assert response.content_type.startswith("text/html")

    def test_health_check_exists(self, client):
        """Test that health check endpoint exists."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert "timestamp" in data

    def test_popular_examples_api_exists(self, client):
        """Test that popular examples API endpoint exists."""
        response = client.get("/api/popular-examples")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "success" in data
        assert "examples" in data

    def test_popular_examples_api_with_count(self, client):
        """Test popular examples API with custom count parameter."""
        response = client.get("/api/popular-examples?count=5")
        assert response.status_code == 200
        data = json.loads(response.data)
        if data["success"]:
            assert len(data["examples"]) == 5

    def test_recommend_endpoint_exists(self, client):
        """Test that recommend endpoint exists (may fail without models)."""
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

        # Endpoint should exist (may return error due to missing models)
        assert response.status_code in [200, 400, 500]


if __name__ == "__main__":
    pytest.main([__file__])
