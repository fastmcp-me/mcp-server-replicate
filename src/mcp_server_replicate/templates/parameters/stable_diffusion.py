"""Parameter templates for Stable Diffusion models."""

from typing import Dict, Any

SDXL_PARAMETERS = {
    "id": "sdxl-base",
    "name": "SDXL Base Parameters",
    "description": "Default parameters for SDXL models",
    "model_type": "stable-diffusion",
    "default_parameters": {
        "width": 1024,
        "height": 1024,
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "prompt_strength": 1.0,
        "refine": "expert_ensemble_refiner",
        "scheduler": "K_EULER",
        "num_outputs": 1,
    },
    "parameter_schema": {
        "type": "object",
        "properties": {
            "prompt": {"type": "string", "description": "Text prompt for image generation"},
            "negative_prompt": {"type": "string", "description": "Text prompt for elements to avoid"},
            "width": {"type": "integer", "minimum": 512, "maximum": 2048, "multipleOf": 8},
            "height": {"type": "integer", "minimum": 512, "maximum": 2048, "multipleOf": 8},
            "num_inference_steps": {"type": "integer", "minimum": 1, "maximum": 100},
            "guidance_scale": {"type": "number", "minimum": 1, "maximum": 20},
            "prompt_strength": {"type": "number", "minimum": 0, "maximum": 1},
            "refine": {"type": "string", "enum": ["no_refiner", "expert_ensemble_refiner", "base_image_refiner"]},
            "scheduler": {"type": "string", "enum": ["DDIM", "DPM_MULTISTEP", "K_EULER"]},
            "num_outputs": {"type": "integer", "minimum": 1, "maximum": 4},
        },
        "required": ["prompt"]
    },
    "version": "1.0.0",
}

SD_15_PARAMETERS = {
    "id": "sd-1.5-base",
    "name": "Stable Diffusion 1.5 Parameters",
    "description": "Default parameters for SD 1.5 models",
    "model_type": "stable-diffusion",
    "default_parameters": {
        "width": 512,
        "height": 512,
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "scheduler": "K_EULER",
        "num_outputs": 1,
    },
    "parameter_schema": {
        "type": "object",
        "properties": {
            "prompt": {"type": "string", "description": "Text prompt for image generation"},
            "negative_prompt": {"type": "string", "description": "Text prompt for elements to avoid"},
            "width": {"type": "integer", "minimum": 256, "maximum": 1024, "multipleOf": 8},
            "height": {"type": "integer", "minimum": 256, "maximum": 1024, "multipleOf": 8},
            "num_inference_steps": {"type": "integer", "minimum": 1, "maximum": 100},
            "guidance_scale": {"type": "number", "minimum": 1, "maximum": 20},
            "scheduler": {"type": "string", "enum": ["DDIM", "DPM_MULTISTEP", "K_EULER"]},
            "num_outputs": {"type": "integer", "minimum": 1, "maximum": 4},
        },
        "required": ["prompt"]
    },
    "version": "1.0.0",
}

# Export all templates
TEMPLATES: Dict[str, Dict[str, Any]] = {
    "sdxl": SDXL_PARAMETERS,
    "sd15": SD_15_PARAMETERS,
} 