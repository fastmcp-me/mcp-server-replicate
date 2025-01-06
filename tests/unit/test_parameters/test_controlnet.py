"""Tests for ControlNet parameter templates."""

import pytest
from typing import Dict, Any

from mcp-server-replicate.templates.parameters.controlnet import (
    TEMPLATES,
    CANNY_PARAMETERS,
    DEPTH_PARAMETERS,
    POSE_PARAMETERS,
    SEGMENTATION_PARAMETERS,
)

def test_templates_export():
    """Test that all templates are properly exported."""
    assert "canny" in TEMPLATES
    assert "depth" in TEMPLATES
    assert "pose" in TEMPLATES
    assert "segmentation" in TEMPLATES

@pytest.mark.parametrize("template", [
    CANNY_PARAMETERS,
    DEPTH_PARAMETERS,
    POSE_PARAMETERS,
    SEGMENTATION_PARAMETERS,
])
def test_template_structure(template: Dict[str, Any]):
    """Test that each template has the required structure."""
    assert "id" in template
    assert "name" in template
    assert "description" in template
    assert "model_type" in template
    assert "control_type" in template
    assert "default_parameters" in template
    assert "parameter_schema" in template
    assert "version" in template
    
    # Check parameter schema structure
    schema = template["parameter_schema"]
    assert schema["type"] == "object"
    assert "properties" in schema
    assert "required" in schema
    
    # Check required base parameters
    properties = schema["properties"]
    assert "prompt" in properties
    assert "image" in properties
    assert "num_inference_steps" in properties
    assert "guidance_scale" in properties
    assert "controlnet_conditioning_scale" in properties
    
    # Check required fields are listed
    assert "prompt" in schema["required"]
    assert "image" in schema["required"]

def test_canny_parameters():
    """Test Canny edge detection specific parameters."""
    template = CANNY_PARAMETERS
    
    # Check Canny-specific parameters
    assert "low_threshold" in template["default_parameters"]
    assert "high_threshold" in template["default_parameters"]
    
    properties = template["parameter_schema"]["properties"]
    assert "low_threshold" in properties
    assert properties["low_threshold"]["type"] == "integer"
    assert properties["low_threshold"]["minimum"] == 1
    assert properties["low_threshold"]["maximum"] == 255
    
    assert "high_threshold" in properties
    assert properties["high_threshold"]["type"] == "integer"
    assert properties["high_threshold"]["minimum"] == 1
    assert properties["high_threshold"]["maximum"] == 255

def test_depth_parameters():
    """Test depth estimation specific parameters."""
    template = DEPTH_PARAMETERS
    
    # Check depth-specific parameters
    assert "detect_resolution" in template["default_parameters"]
    assert "boost" in template["default_parameters"]
    
    properties = template["parameter_schema"]["properties"]
    assert "detect_resolution" in properties
    assert properties["detect_resolution"]["type"] == "integer"
    assert properties["detect_resolution"]["minimum"] == 128
    assert properties["detect_resolution"]["maximum"] == 1024
    
    assert "boost" in properties
    assert properties["boost"]["type"] == "number"
    assert properties["boost"]["minimum"] == 0.0
    assert properties["boost"]["maximum"] == 2.0

def test_pose_parameters():
    """Test pose detection specific parameters."""
    template = POSE_PARAMETERS
    
    # Check pose-specific parameters
    assert "detect_resolution" in template["default_parameters"]
    assert "include_hand_pose" in template["default_parameters"]
    assert "include_face_landmarks" in template["default_parameters"]
    
    properties = template["parameter_schema"]["properties"]
    assert "detect_resolution" in properties
    assert "include_hand_pose" in properties
    assert properties["include_hand_pose"]["type"] == "boolean"
    assert "include_face_landmarks" in properties
    assert properties["include_face_landmarks"]["type"] == "boolean"

def test_segmentation_parameters():
    """Test segmentation specific parameters."""
    template = SEGMENTATION_PARAMETERS
    
    # Check segmentation-specific parameters
    assert "detect_resolution" in template["default_parameters"]
    assert "output_type" in template["default_parameters"]
    
    properties = template["parameter_schema"]["properties"]
    assert "detect_resolution" in properties
    assert "output_type" in properties
    assert properties["output_type"]["type"] == "string"
    assert "ade20k" in properties["output_type"]["enum"]
    assert "coco" in properties["output_type"]["enum"] 