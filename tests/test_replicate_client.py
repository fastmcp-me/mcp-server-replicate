"""Tests for the Replicate API client implementation."""

from unittest.mock import Mock, patch

import pytest
import replicate

from mcp_server_replicate.replicate_client import ReplicateClient


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock Replicate client."""
    client = Mock(spec=replicate.Client)
    monkeypatch.setattr("replicate.Client", lambda: client)
    return client


@pytest.fixture
def mock_version():
    """Create a mock version response."""
    return Mock(
        id="version1",
        created_at=Mock(isoformat=lambda: "2024-01-01T00:00:00Z"),
        cog_version="1.0.0",
        openapi_schema={"type": "object"},
    )


@pytest.fixture
def mock_model(mock_version):
    """Create a mock model response."""
    return Mock(
        owner="test_owner",
        name="test_model",
        description="test_description",
        visibility="public",
        latest_version=mock_version,
    )


@pytest.fixture
def mock_prediction():
    """Create a mock prediction response."""
    return Mock(
        id="test_prediction_id",
        status="succeeded",
        output={"result": "test output"},
        error=None,
        created_at=Mock(isoformat=lambda: "2024-01-01T00:00:00Z"),
        started_at=Mock(isoformat=lambda: "2024-01-01T00:00:01Z"),
        completed_at=Mock(isoformat=lambda: "2024-01-01T00:00:02Z"),
        urls={"get": "https://api.replicate.com/v1/predictions/test_id"},
        metrics={"predict_time": 1.0},
    )


def test_init_with_valid_token():
    """Test client initialization with valid API token."""
    client = ReplicateClient(api_token="test_token")
    assert client.client is not None


def test_init_without_token():
    """Test client initialization fails without API token."""
    client = ReplicateClient(api_token=None)
    assert client.client is None
    assert "Replicate API token is required" in client.error


def test_init_with_empty_token():
    """Test client initialization fails with empty token."""
    client = ReplicateClient(api_token="  ")
    assert client.client is None
    assert "Replicate API token is required" in client.error


def test_list_models(mock_client, mock_model):
    """Test list_models method."""
    # Set up mock response
    mock_models = Mock()
    mock_models.next_cursor = "next_page"
    mock_models.total = 50
    mock_models.__iter__ = Mock(return_value=iter([mock_model]))

    mock_client.models.list.return_value = mock_models

    client = ReplicateClient(api_token="test_token")
    result = client.list_models(owner=None)

    assert len(result["models"]) <= 5
    assert result["next_cursor"] == "next_page"
    assert result["total_models"] == 50

    model = result["models"][0]
    assert model["owner"] == mock_model.owner
    assert model["name"] == mock_model.name
    assert model["latest_version_id"] == mock_model.latest_version.id


def test_list_models_without_pagination(mock_client, mock_model):
    """Test list_models method when pagination info is not available."""
    # Set up mock response without next_cursor and total attributes
    mock_models = Mock()
    # Explicitly remove next_cursor and total attributes
    del mock_models.next_cursor
    del mock_models.total
    mock_models.__iter__ = Mock(return_value=iter([mock_model]))

    mock_client.models.list.return_value = mock_models

    client = ReplicateClient(api_token="test_token")
    result = client.list_models(owner=None)

    assert len(result["models"]) <= 5
    assert result["next_cursor"] is None
    assert result["total_models"] is None

    model = result["models"][0]
    assert model["owner"] == mock_model.owner
    assert model["name"] == mock_model.name
    assert model["latest_version_id"] == mock_model.latest_version.id


def test_list_models_with_owner_filter(mock_client, mock_model):
    """Test list_models method with owner filter."""
    mock_models = Mock()
    mock_models.__iter__ = Mock(return_value=iter([mock_model]))
    mock_client.models.list.return_value = mock_models

    client = ReplicateClient(api_token="test_token")
    result = client.list_models(owner="test_owner")

    assert len(result["models"]) == 1
    assert result["models"][0]["owner"] == "test_owner"


def test_get_model_versions(mock_client, mock_model, mock_version):
    """Test get_model_versions method."""
    mock_model.versions.list.return_value = [mock_version]
    mock_client.models.get.return_value = mock_model

    client = ReplicateClient(api_token="test_token")
    result = client.get_model_versions("owner/model")

    assert len(result) == 1
    assert result[0]["id"] == mock_version.id
    assert result[0]["created_at"] == mock_version.created_at.isoformat()
    assert result[0]["cog_version"] == mock_version.cog_version


def test_get_model_versions_not_found(mock_client):
    """Test get_model_versions with non-existent model."""
    mock_client.models.get.return_value = None

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(ValueError) as exc_info:
        client.get_model_versions("owner/nonexistent")
    assert "Model not found" in str(exc_info.value)


def test_predict(mock_client, mock_model, mock_prediction):
    """Test predict method."""
    mock_model.versions.get.return_value = mock_model.latest_version
    mock_model.latest_version.predict.return_value = mock_prediction
    mock_client.models.get.return_value = mock_model

    client = ReplicateClient(api_token="test_token")
    result = client.predict("owner/model", {"prompt": "test"}, version="test_version")

    assert result["id"] == mock_prediction.id
    assert result["status"] == mock_prediction.status
    assert result["output"] == mock_prediction.output
    assert result["created_at"] == mock_prediction.created_at.isoformat()


def test_predict_model_not_found(mock_client):
    """Test predict with non-existent model."""
    mock_client.models.get.return_value = None

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(ValueError) as exc_info:
        client.predict("owner/nonexistent", {"prompt": "test"})
    assert "Model not found" in str(exc_info.value)


def test_predict_version_not_found(mock_client, mock_model):
    """Test predict with non-existent version."""
    mock_model.versions.get.return_value = None
    mock_client.models.get.return_value = mock_model

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(ValueError) as exc_info:
        client.predict("owner/model", {"prompt": "test"}, version="nonexistent")
    assert "Version not found" in str(exc_info.value)


def test_get_prediction_status(mock_client, mock_prediction):
    """Test get_prediction_status method."""
    mock_client.predictions.get.return_value = mock_prediction

    client = ReplicateClient(api_token="test_token")
    result = client.get_prediction_status("test_id")

    assert result["id"] == mock_prediction.id
    assert result["status"] == mock_prediction.status
    assert result["output"] == mock_prediction.output
    assert result["created_at"] == mock_prediction.created_at.isoformat()
    assert result["urls"] == mock_prediction.urls
    assert result["metrics"] == mock_prediction.metrics


def test_get_prediction_status_not_found(mock_client):
    """Test get_prediction_status with non-existent prediction."""
    mock_client.predictions.get.return_value = None

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(ValueError) as exc_info:
        client.get_prediction_status("nonexistent")
    assert "Prediction not found" in str(exc_info.value)


def test_list_models_api_error(mock_client):
    """Test list_models error handling."""
    mock_client.models.list.side_effect = Exception("API error")

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(Exception) as exc_info:
        client.list_models()
    assert "Failed to list models: API error" in str(exc_info.value)


def test_get_model_versions_api_error(mock_client, mock_model):
    """Test get_model_versions API error handling."""
    mock_client.models.get.return_value = mock_model
    mock_model.versions.list.side_effect = Exception("API error")

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(Exception) as exc_info:
        client.get_model_versions("owner/model")
    assert "Failed to get model versions: API error" in str(exc_info.value)


def test_predict_api_error(mock_client, mock_model):
    """Test predict API error handling."""
    mock_client.models.get.return_value = mock_model
    mock_model.latest_version.predict.side_effect = Exception("API error")

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(Exception) as exc_info:
        client.predict("owner/model", {"prompt": "test"})
    assert "Prediction failed: API error" in str(exc_info.value)


def test_get_prediction_status_api_error(mock_client):
    """Test get_prediction_status API error handling."""
    mock_client.predictions.get.side_effect = Exception("API error")

    client = ReplicateClient(api_token="test_token")
    with pytest.raises(Exception) as exc_info:
        client.get_prediction_status("test_id")
    assert "Failed to get prediction status: API error" in str(exc_info.value)
