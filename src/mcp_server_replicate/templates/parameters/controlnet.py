"""Parameter templates for ControlNet models.

This module defines parameter templates for different types of ControlNet models,
including Canny edge detection, depth estimation, pose detection, and segmentation.
"""

from typing import Dict, Any, Literal

ControlType = Literal["canny", "depth", "pose", "segmentation"]

# Base ControlNet parameters shared across all types
BASE_CONTROLNET_PARAMETERS = {
    "default_parameters": {
        "num_inference_steps": 30,
        "guidance_scale": 7.5,
        "controlnet_conditioning_scale": 1.0,
        "control_guidance_start": 0.0,
        "control_guidance_end": 1.0,
        "scheduler": "K_EULER",
    },
    "parameter_schema": {
        "type": "object",
        "properties": {
            "prompt": {"type": "string", "description": "Text prompt for image generation"},
            "negative_prompt": {"type": "string", "description": "Text prompt for elements to avoid"},
            "image": {"type": "string", "description": "Base64 encoded input image"},
            "num_inference_steps": {"type": "integer", "minimum": 1, "maximum": 100},
            "guidance_scale": {"type": "number", "minimum": 1, "maximum": 20},
            "controlnet_conditioning_scale": {"type": "number", "minimum": 0.0, "maximum": 2.0},
            "control_guidance_start": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "control_guidance_end": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "scheduler": {"type": "string", "enum": ["DDIM", "DPM_MULTISTEP", "K_EULER"]},
        },
        "required": ["prompt", "image"]
    },
}

CANNY_PARAMETERS = {
    "id": "controlnet-canny",
    "name": "ControlNet Canny Parameters",
    "description": "Parameters for ControlNet Canny edge detection models",
    "model_type": "controlnet",
    "control_type": "canny",
    **BASE_CONTROLNET_PARAMETERS,
    "default_parameters": {
        **BASE_CONTROLNET_PARAMETERS["default_parameters"],
        "low_threshold": 100,
        "high_threshold": 200,
    },
    "parameter_schema": {
        "type": "object",
        "properties": {
            **BASE_CONTROLNET_PARAMETERS["parameter_schema"]["properties"],
            "low_threshold": {"type": "integer", "minimum": 1, "maximum": 255},
            "high_threshold": {"type": "integer", "minimum": 1, "maximum": 255},
        },
        "required": BASE_CONTROLNET_PARAMETERS["parameter_schema"]["required"]
    },
    "version": "1.0.0",
}

DEPTH_PARAMETERS = {
    "id": "controlnet-depth",
    "name": "ControlNet Depth Parameters",
    "description": "Parameters for ControlNet depth estimation models",
    "model_type": "controlnet",
    "control_type": "depth",
    **BASE_CONTROLNET_PARAMETERS,
    "default_parameters": {
        **BASE_CONTROLNET_PARAMETERS["default_parameters"],
        "detect_resolution": 512,
        "boost": 1.0,
    },
    "parameter_schema": {
        "type": "object",
        "properties": {
            **BASE_CONTROLNET_PARAMETERS["parameter_schema"]["properties"],
            "detect_resolution": {"type": "integer", "minimum": 128, "maximum": 1024},
            "boost": {"type": "number", "minimum": 0.0, "maximum": 2.0},
        },
        "required": BASE_CONTROLNET_PARAMETERS["parameter_schema"]["required"]
    },
    "version": "1.0.0",
}

POSE_PARAMETERS = {
    "id": "controlnet-pose",
    "name": "ControlNet Pose Parameters",
    "description": "Parameters for ControlNet pose detection models",
    "model_type": "controlnet",
    "control_type": "pose",
    **BASE_CONTROLNET_PARAMETERS,
    "default_parameters": {
        **BASE_CONTROLNET_PARAMETERS["default_parameters"],
        "detect_resolution": 512,
        "include_hand_pose": True,
        "include_face_landmarks": True,
    },
    "parameter_schema": {
        "type": "object",
        "properties": {
            **BASE_CONTROLNET_PARAMETERS["parameter_schema"]["properties"],
            "detect_resolution": {"type": "integer", "minimum": 128, "maximum": 1024},
            "include_hand_pose": {"type": "boolean"},
            "include_face_landmarks": {"type": "boolean"},
        },
        "required": BASE_CONTROLNET_PARAMETERS["parameter_schema"]["required"]
    },
    "version": "1.0.0",
}

SEGMENTATION_PARAMETERS = {
    "id": "controlnet-segmentation",
    "name": "ControlNet Segmentation Parameters",
    "description": "Parameters for ControlNet segmentation models",
    "model_type": "controlnet",
    "control_type": "segmentation",
    **BASE_CONTROLNET_PARAMETERS,
    "default_parameters": {
        **BASE_CONTROLNET_PARAMETERS["default_parameters"],
        "detect_resolution": 512,
        "output_type": "ade20k",  # ADE20K segmentation format
    },
    "parameter_schema": {
        "type": "object",
        "properties": {
            **BASE_CONTROLNET_PARAMETERS["parameter_schema"]["properties"],
            "detect_resolution": {"type": "integer", "minimum": 128, "maximum": 1024},
            "output_type": {"type": "string", "enum": ["ade20k", "coco"]},
        },
        "required": BASE_CONTROLNET_PARAMETERS["parameter_schema"]["required"]
    },
    "version": "1.0.0",
}

# Export all templates
TEMPLATES: Dict[str, Dict[str, Any]] = {
    "canny": CANNY_PARAMETERS,
    "depth": DEPTH_PARAMETERS,
    "pose": POSE_PARAMETERS,
    "segmentation": SEGMENTATION_PARAMETERS,
} 