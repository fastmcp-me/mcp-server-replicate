#!/usr/bin/env python3
"""MCP Server implementation for the Replicate API."""

import logging
import sys
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context

from .replicate_client import ReplicateClient

# Configure minimal logging
logging.basicConfig(
    level=logging.WARNING,  # Only log warnings and above
    format="%(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def register_tools(server: FastMCP, client: ReplicateClient) -> None:
    """Register all tools with the server.

    Args:
        server: FastMCP server instance
        client: ReplicateClient instance
    """

    @server.tool()
    async def predict(
        ctx: Context,
        model: str,  # Model identifier (e.g., 'owner/model')
        input: Dict[str, Any],  # Model-specific input parameters
        version: str | None = None,  # Optional model version hash
    ) -> Dict[str, Any]:
        """Run a prediction using a Replicate model."""
        try:
            result = client.predict(model, input, version)
            return {"content": result}
        except Exception as err:
            logger.error(f"Prediction failed: {str(err)}")
            raise

    @server.tool()
    async def list_models(
        ctx: Context,
        owner: str | None = None,  # Optional owner filter
        cursor: str | None = None,  # Pagination cursor
    ) -> Dict[str, Any]:
        """List available models on Replicate with pagination."""
        try:
            result = client.list_models(owner, cursor)
            return {"content": result}
        except Exception as err:
            logger.error(f"Failed to list models: {str(err)}")
            raise

    @server.tool()
    async def get_model_versions(
        ctx: Context,
        model: str,  # Model identifier (e.g., 'owner/model')
    ) -> Dict[str, Any]:
        """Get available versions for a model."""
        try:
            result = client.get_model_versions(model)
            return {"content": {"versions": result}}
        except Exception as err:
            logger.error(f"Failed to get model versions: {str(err)}")
            raise

    @server.tool()
    async def get_prediction_status(
        ctx: Context,
        prediction_id: str,  # Prediction ID to check status for
    ) -> Dict[str, Any]:
        """Get the status of a prediction."""
        try:
            result = client.get_prediction_status(prediction_id)
            return {"content": result}
        except Exception as err:
            logger.error(f"Failed to get prediction status: {str(err)}")
            raise


def create_server(api_token: str | None = None) -> tuple[FastMCP, ReplicateClient]:
    """Create and initialize the Replicate MCP server.

    Args:
        api_token: Optional Replicate API token for authentication
    """
    # Initialize ReplicateClient with API token
    client = ReplicateClient(api_token=api_token)

    # Initialize FastMCP server
    server = FastMCP(
        name="replicate-server",
        version="0.1.0",
        capabilities={
            "tools": {
                "predict": {
                    "description": "Run a prediction using a Replicate model",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "model": {"type": "string", "description": "Model identifier (e.g., 'owner/model')"},
                            "input": {"type": "object", "description": "Model-specific input parameters"},
                            "version": {"type": "string", "description": "Optional model version hash"},
                        },
                        "required": ["model", "input"],
                    },
                },
                "list_models": {
                    "description": "List available models on Replicate with pagination",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "owner": {"type": "string", "description": "Optional owner filter"},
                            "cursor": {"type": "string", "description": "Pagination cursor"},
                        },
                    },
                },
                "get_model_versions": {
                    "description": "Get available versions for a model",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "model": {"type": "string", "description": "Model identifier (e.g., 'owner/model')"}
                        },
                        "required": ["model"],
                    },
                },
                "get_prediction_status": {
                    "description": "Get the status of a prediction",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "prediction_id": {"type": "string", "description": "ID of the prediction to check"}
                        },
                        "required": ["prediction_id"],
                    },
                },
            }
        },
    )

    # Register tools with ReplicateClient
    register_tools(server, client)

    return server, client


def main():
    """Entry point for the MCP server."""
    import os

    # Create server instance with API token from environment
    server, client = create_server(api_token=os.getenv("REPLICATE_API_TOKEN"))
    # Run server in direct execution mode
    server.run()


if __name__ == "__main__":
    main()
