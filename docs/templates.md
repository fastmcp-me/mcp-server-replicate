# Template Documentation

## Overview

This document provides comprehensive documentation for all templates available in the MCP Server for Replicate. Templates are organized into several categories:

1. Model Parameters
2. Common Configurations
3. Prompt Templates

## Model Parameters

### SDXL Parameters

The SDXL template provides parameters optimized for Stable Diffusion XL models.

```python
{
    "prompt": "your detailed prompt",
    "negative_prompt": "elements to avoid",
    "width": 1024,  # 512-2048, multiple of 8
    "height": 1024,  # 512-2048, multiple of 8
    "num_inference_steps": 50,  # 1-150
    "guidance_scale": 7.5,  # 1-20
    "prompt_strength": 1.0,  # 0-1
    "refine": "expert_ensemble_refiner",  # or "no_refiner", "base_image_refiner"
    "scheduler": "K_EULER",  # or "DDIM", "DPM_MULTISTEP", "PNDM", "KLMS"
    "num_outputs": 1,  # 1-4
    "high_noise_frac": 0.8,  # 0-1
    "seed": null,  # null or integer
    "apply_watermark": true
}
```

### SD 1.5 Parameters

The SD 1.5 template provides parameters optimized for Stable Diffusion 1.5 models.

```python
{
    "prompt": "your detailed prompt",
    "negative_prompt": "elements to avoid",
    "width": 512,  # 256-1024, multiple of 8
    "height": 512,  # 256-1024, multiple of 8
    "num_inference_steps": 50,  # 1-150
    "guidance_scale": 7.5,  # 1-20
    "scheduler": "K_EULER",  # or "DDIM", "DPM_MULTISTEP", "PNDM", "KLMS"
    "num_outputs": 1,  # 1-4
    "seed": null,  # null or integer
    "apply_watermark": true
}
```

### ControlNet Parameters

The ControlNet template provides parameters for controlled image generation.

```python
{
    "control_image": "image_url_or_base64",
    "control_mode": "balanced",  # or "prompt", "control"
    "control_scale": 0.9,  # 0-2
    "begin_control_step": 0.0,  # 0-1
    "end_control_step": 1.0,  # 0-1
    "detection_resolution": 512,  # 256-1024, multiple of 8
    "image_resolution": 512,  # 256-1024, multiple of 8
    "guess_mode": false,
    "preprocessor": "canny"  # or other preprocessors
}
```

## Common Configurations

### Quality Presets

Pre-configured quality settings for different use cases:

- `draft`: Fast iterations (20 steps)
- `balanced`: General use (30 steps)
- `quality`: High quality (50 steps)
- `extreme`: Maximum quality (150 steps)

### Style Presets

Pre-configured style settings:

- `photorealistic`: Highly detailed photo style
- `cinematic`: Movie-like dramatic style
- `anime`: Anime/manga style
- `digital_art`: Modern digital art style
- `oil_painting`: Classical painting style

### Aspect Ratio Presets

Common aspect ratios with optimal resolutions:

- `square`: 1:1 (1024x1024)
- `portrait`: 2:3 (832x1216)
- `landscape`: 3:2 (1216x832)
- `wide`: 16:9 (1344x768)
- `mobile`: 9:16 (768x1344)

### Negative Prompt Presets

Quality control negative prompts:

- `quality_control`: Basic quality control
- `strict_quality`: Comprehensive quality control
- `photo_quality`: Photo-specific quality control
- `artistic_quality`: Art-specific quality control

## Prompt Templates

### Text-to-Image

#### Detailed Scene Template

```
{subject} in {setting}, {lighting} lighting, {mood} atmosphere, {style} style, {details}
```

Example:

```
"a young explorer in ancient temple ruins, dramatic golden hour lighting, mysterious atmosphere, cinematic style, vines growing on weathered stone, dust particles in light beams"
```

#### Character Portrait Template

```
{gender} {character_type}, {appearance}, {clothing}, {expression}, {pose}, {style} style, {background}
```

#### Landscape Template

```
{environment} landscape, {time_of_day}, {weather}, {features}, {style} style, {mood} mood
```

### Image-to-Image

#### Style Transfer Template

```
Transform into {style} style, {quality} quality, maintain {preserve} from original
```

#### Variation Template

```
Similar to original but with {changes}, {style} style, {quality} quality
```

### ControlNet

#### Pose-Guided Template

```
{subject} in {pose_description}, {clothing}, {style} style, {background}
```

#### Depth-Guided Template

```
{subject} with {depth_elements}, {perspective}, {style} style
```

## Best Practices

1. **Parameter Selection**

   - Start with preset configurations
   - Adjust parameters gradually
   - Use appropriate aspect ratios for your use case

2. **Prompt Engineering**

   - Use detailed, specific descriptions
   - Include style and quality indicators
   - Use negative prompts for quality control

3. **ControlNet Usage**

   - Match detection and output resolutions
   - Use appropriate preprocessors for your use case
   - Adjust control scale based on desired influence

4. **Quality Optimization**
   - Use higher step counts for final outputs
   - Adjust guidance scale for creativity vs. accuracy
   - Use refiners for enhanced quality

## Version History

- v1.1.0: Added comprehensive parameter descriptions and validation
- v1.0.0: Initial release with basic parameters
