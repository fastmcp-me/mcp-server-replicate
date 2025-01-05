"""Tests for the FastMCP server implementation."""

import importlib
import logging
import os
from unittest.mock import Mock, patch

import pytest
from mcp.server.fastmcp import FastMCP

from mcp_server_replicate.replicate_client import ReplicateClient


@pytest.fixture
def mock_replicate_client():
    """Create a mock ReplicateClient."""
    mock = Mock(spec=ReplicateClient)
    # Mock the client property to avoid auth errors
    mock.client = Mock()
    mock.client.models = Mock()
    mock.client.predictions = Mock()
    return mock


@pytest.fixture
def server_module():
    """Import the server module."""
    return importlib.import_module("mcp_server_replicate.server")


@pytest.fixture
def server(mock_replicate_client):
    """Create a FastMCP server instance with mocked client."""
    with patch("mcp_server_replicate.server.ReplicateClient", return_value=mock_replicate_client):
        server_module = importlib.import_module("mcp_server_replicate.server")
        server, _ = server_module.create_server(api_token="test_token")
        return server


@pytest.mark.asyncio
async def test_server_tools_registered(server):
    """Test that all tools are properly registered with the server."""
    tools = await server.list_tools()

    expected_tools = ["predict", "list_models", "get_model_versions", "get_prediction_status"]
    registered_tools = [tool.name for tool in tools]
    assert set(registered_tools) == set(expected_tools)


@pytest.mark.asyncio
async def test_predict_tool(server, mock_replicate_client):
    """Test predict tool delegates to ReplicateClient."""
    mock_replicate_client.predict.return_value = {"id": "test", "status": "succeeded"}

    result = await server.call_tool(
        "predict", {"model": "owner/model", "input": {"prompt": "test"}, "version": "test_version"}
    )

    mock_replicate_client.predict.assert_called_once_with("owner/model", {"prompt": "test"}, "test_version")
    assert len(result) == 1
    content = result[0].text
    assert '"id": "test"' in content
    assert '"status": "succeeded"' in content


@pytest.mark.asyncio
async def test_list_models_tool(server, mock_replicate_client):
    """Test list_models tool delegates to ReplicateClient."""
    mock_replicate_client.list_models.return_value = {
        "models": [{"name": "test"}],
        "next_cursor": "next",
        "total_models": 1,
    }

    result = await server.call_tool("list_models", {"owner": "test_owner", "cursor": "test_cursor"})

    mock_replicate_client.list_models.assert_called_once_with("test_owner", "test_cursor")
    assert len(result) == 1
    content = result[0].text
    assert '"models": [{"name": "test"}]' in content
    assert '"next_cursor": "next"' in content


@pytest.mark.asyncio
async def test_get_model_versions_tool(server, mock_replicate_client):
    """Test get_model_versions tool delegates to ReplicateClient."""
    mock_replicate_client.get_model_versions.return_value = [{"id": "v1", "created_at": "2024-01-01T00:00:00Z"}]

    result = await server.call_tool("get_model_versions", {"model": "owner/model"})

    mock_replicate_client.get_model_versions.assert_called_once_with("owner/model")
    assert len(result) == 1
    content = result[0].text
    assert '"versions": [{"id": "v1"' in content


@pytest.mark.asyncio
async def test_get_prediction_status_tool(server, mock_replicate_client):
    """Test get_prediction_status tool delegates to ReplicateClient."""
    mock_replicate_client.get_prediction_status.return_value = {"id": "test_id", "status": "succeeded"}

    result = await server.call_tool("get_prediction_status", {"prediction_id": "test_id"})

    mock_replicate_client.get_prediction_status.assert_called_once_with("test_id")
    assert len(result) == 1
    content = result[0].text
    assert '"id": "test_id"' in content
    assert '"status": "succeeded"' in content


@pytest.mark.asyncio
async def test_tool_error_handling(server, mock_replicate_client):
    """Test error handling in tools."""
    mock_replicate_client.predict.side_effect = ValueError("Test error")

    with pytest.raises(Exception) as exc_info:
        await server.call_tool("predict", {"model": "owner/model", "input": {"prompt": "test"}})
    assert "Test error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_tool_error_propagation(server, mock_replicate_client):
    """Test error propagation from ReplicateClient."""
    mock_replicate_client.predict.side_effect = Exception("API error")

    with pytest.raises(Exception) as exc_info:
        await server.call_tool("predict", {"model": "owner/model", "input": {"prompt": "test"}})
    assert "API error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_tool_validation_error(server, mock_replicate_client):
    """Test input validation error handling."""
    with pytest.raises(Exception) as exc_info:
        await server.call_tool("predict", {"model": "owner/model"})  # Missing required 'input' parameter
    assert "missing" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_server_initialization():
    """Test server initialization."""
    server_module = importlib.import_module("mcp_server_replicate.server")
    server, client = server_module.create_server(api_token="test_token")
    assert isinstance(server, FastMCP)
    assert isinstance(client, ReplicateClient)
    assert client.client is not None


@pytest.mark.asyncio
async def test_tool_error_logging(server, mock_replicate_client, caplog):
    """Test error logging in tool functions."""
    caplog.set_level(logging.ERROR)

    # Test predict tool error logging
    mock_replicate_client.predict.side_effect = Exception("Prediction error")
    with pytest.raises(Exception):
        await server.call_tool("predict", {"model": "owner/model", "input": {"prompt": "test"}})
    assert "Prediction failed: Prediction error" in caplog.text

    caplog.clear()

    # Test list_models tool error logging
    mock_replicate_client.list_models.side_effect = Exception("List error")
    with pytest.raises(Exception):
        await server.call_tool("list_models", {})
    assert "Failed to list models: List error" in caplog.text

    caplog.clear()

    # Test get_model_versions tool error logging
    mock_replicate_client.get_model_versions.side_effect = Exception("Version error")
    with pytest.raises(Exception):
        await server.call_tool("get_model_versions", {"model": "owner/model"})
    assert "Failed to get model versions: Version error" in caplog.text

    caplog.clear()

    # Test get_prediction_status tool error logging
    mock_replicate_client.get_prediction_status.side_effect = Exception("Status error")
    with pytest.raises(Exception):
        await server.call_tool("get_prediction_status", {"prediction_id": "test_id"})
    assert "Failed to get prediction status: Status error" in caplog.text


def test_main_execution():
    """Test main function execution."""
    with (
        patch.dict(os.environ, {"REPLICATE_API_TOKEN": "test_token"}),
        patch("mcp_server_replicate.server.FastMCP.run") as mock_run,
    ):
        from mcp_server_replicate.server import main

        main()
        mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_server_tools(server):
    """Test server tools are properly configured."""
    tools = await server.list_tools()

    # Verify all tools are registered
    tool_names = {tool.name for tool in tools}
    assert "predict" in tool_names
    assert "list_models" in tool_names
    assert "get_model_versions" in tool_names
    assert "get_prediction_status" in tool_names

    # Verify tool schemas
    for tool in tools:
        if tool.name == "predict":
            schema = tool.inputSchema
            assert "model" in schema["required"]
            assert "input" in schema["required"]
            assert "version" in schema["properties"]
