"""Global test configuration and fixtures."""

import pytest
from typing import AsyncGenerator, Dict, Any
from pathlib import Path

# Add project root to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "fixtures" / "data"

@pytest.fixture
def mock_api_responses() -> Dict[str, Any]:
    """Return mock API responses for testing."""
    return {
        "models": {
            "list": {
                "previous": None,
                "next": None,
                "results": [
                    {
                        "url": "https://replicate.com/stability-ai/sdxl",
                        "owner": "stability-ai",
                        "name": "sdxl",
                        "description": "A text-to-image generative AI model",
                        "visibility": "public",
                        "github_url": None,
                        "paper_url": None,
                        "license_url": None,
                        "latest_version": {
                            "id": "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                            "created_at": "2023-09-22T21:00:00.000Z",
                        }
                    }
                ]
            }
        },
        "predictions": {
            "create": {
                "id": "test-prediction-id",
                "version": "test-version-id",
                "status": "starting",
                "created_at": "2024-01-06T00:00:00.000Z",
                "started_at": None,
                "completed_at": None,
                "urls": {
                    "get": "https://api.replicate.com/v1/predictions/test-prediction-id",
                    "cancel": "https://api.replicate.com/v1/predictions/test-prediction-id/cancel",
                }
            },
            "get": {
                "id": "test-prediction-id",
                "version": "test-version-id",
                "status": "succeeded",
                "created_at": "2024-01-06T00:00:00.000Z",
                "started_at": "2024-01-06T00:00:01.000Z",
                "completed_at": "2024-01-06T00:00:10.000Z",
                "output": ["https://replicate.delivery/test-output.png"],
                "urls": {
                    "get": "https://api.replicate.com/v1/predictions/test-prediction-id",
                    "cancel": "https://api.replicate.com/v1/predictions/test-prediction-id/cancel",
                }
            }
        }
    }

@pytest.fixture
async def mock_client() -> AsyncGenerator[Dict[str, Any], None]:
    """Return a mock client for testing."""
    client = {
        "api_token": "test-token",
        "base_url": "https://api.replicate.com/v1",
        "responses": mock_api_responses(),
    }
    yield client 