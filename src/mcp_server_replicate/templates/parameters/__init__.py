"""Parameter templates for various model types.

This module exports parameter templates for different model types including:
- Stable Diffusion (SD 1.5 and SDXL)
- LLaMA language models
- ControlNet variants (Canny, Depth, Pose, Segmentation)
"""

from typing import Dict, Any

from .stable_diffusion import TEMPLATES as SD_TEMPLATES
from .llama import TEMPLATES as LLAMA_TEMPLATES
from .controlnet import TEMPLATES as CONTROLNET_TEMPLATES

# Combine all templates with namespaced keys
TEMPLATES: Dict[str, Dict[str, Any]] = {
    # Stable Diffusion templates
    "sd/sdxl": SD_TEMPLATES["sdxl"],
    "sd/sd15": SD_TEMPLATES["sd15"],
    
    # LLaMA templates
    **{f"llama/{k}": v for k, v in LLAMA_TEMPLATES.items()},
    
    # ControlNet templates
    "controlnet/canny": CONTROLNET_TEMPLATES["canny"],
    "controlnet/depth": CONTROLNET_TEMPLATES["depth"],
    "controlnet/pose": CONTROLNET_TEMPLATES["pose"],
    "controlnet/segmentation": CONTROLNET_TEMPLATES["segmentation"],
}

__all__ = ["TEMPLATES"] 