---
name: interior-design-pro
description: Professional interior design image generation with structure preservation. Use for room reskinning, style transfer, and surface inpainting while keeping exact room geometry.
---

# Interior Design Pro

Enterprise-level interior design generation using ControlNet structure preservation.

## Core Principle: RESKIN, Don't Rebuild

**We are decorators, not builders.**

The architecture (windows, doors, walls, ceilings, floor layout) must remain **IDENTICAL**.
Only surfaces change: cabinet fronts, countertops, flooring material, wall colors, fixtures.

## Proven Settings (January 2026)

```python
output = replicate.run(
    'xlabs-ai/flux-dev-controlnet:9a8db105db745f8b11ad3afe5c8bd892428b2a43ade0b67edc4e0ccd52ff2fda',
    input={
        'control_image': open(image_path, 'rb'),
        'prompt': '[structured prompt - see below]',
        'negative_prompt': '[structural blockers - see below]',
        'guidance_scale': 2.5-3.0,      # Lower = less creative drift
        'control_strength': 0.8-0.85,   # High = strict structure
        'image_to_image_strength': 0.1-0.12,  # Anchors original
        'steps': 40,                    # More = smoother lines
        'control_type': 'depth',        # or 'canny' for edges
        'output_format': 'png',
        'output_quality': 100,
    }
)
```

## Prompt Engineering

### Structure (in order):
1. **Style declaration**: "Same kitchen reskinned [STYLE] style"
2. **Surface changes**: "terracotta countertops, wood cabinet fronts, brass fixtures"
3. **PRESERVE block**: "PRESERVE EXACTLY: [list all structural elements]"
4. **Light sources**: "bi-fold doors on LEFT as main light source"
5. **Negative constraints**: "NO windows on right, same island position"
6. **Quality tags**: "professional architectural photography, photorealistic, clean sharp lines"

### Example Prompt:
```
Same kitchen reskinned Mediterranean Moroccan style, terracotta tile 
countertops, decorative zellige tile backsplash, warm rustic wood cabinet 
fronts, brass fixtures and hardware, terracotta and earth tones, 
PRESERVE EXACTLY: bi-fold glass doors on LEFT side, NO windows on right 
side, same large central island, same coffered ceiling, same herringbone 
floor in warm wood, same dining area on left, reskin surfaces only, 
professional architectural photography, photorealistic, ultra high detail, 
clean sharp lines
```

### Negative Prompt Template:
```
windows on right, changed layout, moved island, structural changes, 
new openings, archways where there are none, blurry, soft focus, 
wobbly lines, distorted, different proportions
```

## Pre-Flight Checklist

Before generating, AUDIT the original image:

1. **Light Sources**
   - [ ] Where are windows? (left/right/back)
   - [ ] Where are doors?
   - [ ] Light direction (affects shadows)

2. **Fixed Elements**
   - [ ] Ceiling type (coffered, flat, beamed)
   - [ ] Floor pattern (herringbone, planks, tile)
   - [ ] Wall positions
   - [ ] Built-in appliances

3. **Furniture/Islands**
   - [ ] Position in room
   - [ ] Shape and size
   - [ ] Relationship to other elements

## Control Type Guide

| Type | Best For | Notes |
|------|----------|-------|
| `depth` | General reskins | Smooth results, good structure |
| `canny` | Edge precision | Can be jaggedy, very accurate lines |
| `soft_edge` | Organic shapes | Smoother than canny |

## Quality Tips

- **High-res input = better output** (always request best quality source)
- **40 steps minimum** for clean lines (28 is faster but rougher)
- **100% output quality** for client work
- **Lower guidance (2.5-3.0)** reduces creative drift

## Common Failures & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Added windows | Model being creative | Explicit "NO windows on [side]" |
| Island moved/changed | Low control strength | Increase to 0.85+ |
| Wobbly lines | Low steps | Increase to 40+ |
| Wrong proportions | Poor source image | Request higher resolution |
| Style too subtle | High control strength | Try 0.75-0.8 |

## Style Library

Proven style prompts:

**Mediterranean Moroccan:**
```
terracotta tile countertops, decorative zellige tile backsplash, 
warm rustic wood cabinet fronts, brass fixtures, terracotta and earth tones
```

**Modern Minimalist:**
```
handleless white cabinets, quartz countertops, integrated appliances,
clean lines, neutral palette, minimal hardware
```

**Industrial:**
```
exposed concrete, steel fixtures, raw materials, metal shelving,
Edison bulb lighting, reclaimed wood accents
```

**Scandinavian:**
```
light oak wood, white walls, natural textures, minimal decor,
warm lighting, hygge atmosphere
```

## Cost

~$0.04-0.06 per generation via Replicate (40 steps costs slightly more)

## Version History

- **2026-01-29**: Initial breakthrough with Oliver. Discovered working settings for strict structure preservation.
