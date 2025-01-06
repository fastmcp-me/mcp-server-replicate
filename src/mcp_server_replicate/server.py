"""FastMCP server implementation for Replicate API."""

import os
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
import jsonschema

from .templates.parameters import TEMPLATES
from .replicate_client import ReplicateClient

logger = logging.getLogger(__name__)

class TemplateInput(BaseModel):
    """Input for template-based operations."""
    
    template: str = Field(..., description="Template identifier")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Template parameters")
    
    @field_validator("template")
    def validate_template(cls, v: str) -> str:
        """Validate template identifier."""
        if v not in TEMPLATES:
            raise ValueError(f"Unknown template: {v}")
        return v
    
    @field_validator("parameters")
    def validate_parameters(cls, v: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate template parameters."""
        if "template" not in values:
            return v
        
        template = TEMPLATES[values["template"]]
        try:
            jsonschema.validate(v, template["parameter_schema"])
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Invalid parameters: {e.message}")
        return v

class PredictionInput(BaseModel):
    """Input for prediction operations."""
    
    version: str = Field(..., description="Model version ID")
    input: Dict[str, Any] = Field(..., description="Model input parameters")
    webhook: Optional[str] = Field(None, description="Webhook URL for prediction updates")
    
    @field_validator("input")
    def validate_input(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate prediction input."""
        if not isinstance(v, dict):
            raise ValueError("Input must be a dictionary")
        return v

class ReplicateServer(FastMCP):
    """FastMCP server for Replicate API."""
    
    async def create_prediction(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new prediction."""
        prediction_input = PredictionInput(**input)
        async with ReplicateClient() as client:
            response = await client.create_prediction(
                version=prediction_input.version,
                input=prediction_input.input,
                webhook=prediction_input.webhook,
            )
            return await response.json()
    
    create_prediction.description = "Create a new prediction using a specific model version on Replicate. Provide the version ID and model-specific input parameters."

async def create_server() -> FastMCP:
    """Create and configure the FastMCP server."""
    server = ReplicateServer()
    return server
