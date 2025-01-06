"""Tests for FastMCP server implementation."""

import json
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from mcp-server-replicate.server import create_server
from mcp-server-replicate.models.model import Model, ModelList
from mcp-server-replicate.models.collection import Collection, CollectionList
from mcp-server-replicate.models.hardware import Hardware, HardwareList
from mcp-server-replicate.models.webhook import WebhookPayload

# Test data
MOCK_MODEL = {
    "owner": "stability-ai",
    "name": "sdxl",
    "description": "Stable Diffusion XL",
    "visibility": "public",
    "latest_version_id": "v1.0.0",
    "latest_version_created_at": "2024-01-01T00:00:00Z"
}

MOCK_COLLECTION = {
    "name": "Text to Image",
    "slug": "text-to-image",
    "description": "Models for generating images from text"
}

MOCK_HARDWARE = {
    "name": "GPU T4",
    "sku": "gpu-t4"
}

MOCK_PREDICTION = {
    "id": "pred_123",
    "status": "succeeded",
    "input": {"prompt": "test"},
    "output": "result",
    "created_at": "2024-01-01T00:00:00Z"
}

@pytest.fixture
async def server():
    """Create server instance for testing."""
    return create_server(log_level=0)

@pytest.fixture
def mock_client():
    """Create mock ReplicateClient."""
    with patch("mcp-server-replicate.server.ReplicateClient") as mock:
        client = AsyncMock()
        mock.return_value.__aenter__.return_value = client
        yield client

# Model Tools Tests
async def test_list_models(server, mock_client):
    """Test list_models tool."""
    mock_client.list_models.return_value = {
        "models": [MOCK_MODEL],
        "next_cursor": "next",
        "total_models": 1
    }
    
    result = await server.tools["list_models"].func()
    assert isinstance(result, ModelList)
    assert len(result.models) == 1
    assert result.models[0].owner == MOCK_MODEL["owner"]
    assert result.next_cursor == "next"
    assert result.total_count == 1

async def test_search_models(server, mock_client):
    """Test search_models tool."""
    mock_client.search_models.return_value = {
        "models": [MOCK_MODEL],
        "next_cursor": None,
        "total_models": 1
    }
    
    result = await server.tools["search_models"].func(query="stable diffusion")
    assert isinstance(result, ModelList)
    assert len(result.models) == 1
    assert result.models[0].name == MOCK_MODEL["name"]

# Collection Tools Tests
async def test_list_collections(server, mock_client):
    """Test list_collections tool."""
    mock_client.list_collections.return_value = [MOCK_COLLECTION]
    
    result = await server.tools["list_collections"].func()
    assert isinstance(result, CollectionList)
    assert len(result.collections) == 1
    assert result.collections[0].name == MOCK_COLLECTION["name"]

async def test_get_collection_details(server, mock_client):
    """Test get_collection_details tool."""
    mock_client.get_collection.return_value = MOCK_COLLECTION
    
    result = await server.tools["get_collection_details"].func(collection_slug="text-to-image")
    assert isinstance(result, Collection)
    assert result.name == MOCK_COLLECTION["name"]
    assert result.slug == MOCK_COLLECTION["slug"]

# Hardware Tools Tests
async def test_list_hardware(server, mock_client):
    """Test list_hardware tool."""
    mock_client.list_hardware.return_value = [MOCK_HARDWARE]
    
    result = await server.tools["list_hardware"].func()
    assert isinstance(result, HardwareList)
    assert len(result.hardware) == 1
    assert result.hardware[0].name == MOCK_HARDWARE["name"]

# Template Tools Tests
async def test_list_templates(server):
    """Test list_templates tool."""
    result = await server.tools["list_templates"].func()
    assert isinstance(result, dict)
    for template in result.values():
        assert "schema" in template
        assert "description" in template
        assert "version" in template

async def test_validate_template_parameters(server):
    """Test validate_template_parameters tool."""
    # This requires actual template data from TEMPLATES
    with pytest.raises(ValueError):
        await server.tools["validate_template_parameters"].func({"template": "invalid"})

# Prediction Tools Tests
async def test_create_prediction(server, mock_client):
    """Test create_prediction tool."""
    mock_client.create_prediction.return_value.json.return_value = MOCK_PREDICTION
    
    result = await server.tools["create_prediction"].func({
        "version": "v1",
        "input": {"prompt": "test"}
    })
    assert result["id"] == MOCK_PREDICTION["id"]
    assert result["status"] == MOCK_PREDICTION["status"]

async def test_get_prediction(server, mock_client):
    """Test get_prediction tool."""
    mock_client.get_prediction.return_value.json.return_value = MOCK_PREDICTION
    
    result = await server.tools["get_prediction"].func("pred_123")
    assert result["id"] == MOCK_PREDICTION["id"]
    assert result["status"] == MOCK_PREDICTION["status"]

async def test_cancel_prediction(server, mock_client):
    """Test cancel_prediction tool."""
    mock_client.cancel_prediction.return_value.json.return_value = {
        **MOCK_PREDICTION,
        "status": "canceled"
    }
    
    result = await server.tools["cancel_prediction"].func("pred_123")
    assert result["id"] == MOCK_PREDICTION["id"]
    assert result["status"] == "canceled"

# Webhook Tools Tests
async def test_get_webhook_secret(server, mock_client):
    """Test get_webhook_secret tool."""
    mock_client.get_webhook_secret.return_value = "secret123"
    
    result = await server.tools["get_webhook_secret"].func()
    assert result == "secret123"

async def test_verify_webhook(server):
    """Test verify_webhook tool."""
    payload = WebhookPayload(
        id="evt_123",
        created_at=datetime.now(),
        type="prediction.completed",
        data={"prediction": MOCK_PREDICTION}
    )
    secret = "test_secret"
    
    # Calculate valid signature
    payload_str = json.dumps(payload.model_dump(), sort_keys=True)
    import hmac, hashlib
    signature = hmac.new(
        secret.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Test valid signature
    result = await server.tools["verify_webhook"].func(payload, signature, secret)
    assert result is True
    
    # Test invalid signature
    result = await server.tools["verify_webhook"].func(payload, "invalid", secret)
    assert result is False
    
    # Test empty signature
    result = await server.tools["verify_webhook"].func(payload, "", secret)
    assert result is False 