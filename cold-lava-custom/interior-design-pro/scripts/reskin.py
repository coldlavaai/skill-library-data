#!/usr/bin/env python3
"""
Pro interior design generation using Replicate + ControlNet.
Preserves exact room structure while changing surfaces/style.
"""

import argparse
import json
import os
import sys

try:
    import replicate
except ImportError:
    print(json.dumps({"ok": False, "error": "replicate library required: pip install replicate"}))
    sys.exit(1)

# Style prompt library
STYLE_PROMPTS = {
    "modern": "modern minimalist interior design, clean lines, neutral palette, uncluttered",
    "scandinavian": "Scandinavian interior design, light wood, white walls, cozy textiles, hygge",
    "industrial": "industrial interior design, exposed brick, metal accents, raw materials",
    "midcentury": "mid-century modern interior, warm wood tones, organic shapes, vintage",
    "contemporary": "contemporary interior design, sophisticated finishes, elegant",
    "farmhouse": "modern farmhouse interior, shiplap, natural materials, rustic charm",
    "coastal": "coastal interior design, light blue accents, natural textures, airy",
    "bohemian": "bohemian interior design, eclectic patterns, plants, warm colors",
}


def reskin_room(image_url: str, style: str, room_type: str = "interior", 
                preserve: float = 0.75) -> dict:
    """
    Reskin a room using ControlNet to preserve structure.
    
    Args:
        image_url: URL to source image
        style: Style description or key from STYLE_PROMPTS
        room_type: Type of room (kitchen, bedroom, etc.)
        preserve: Structure preservation strength (0.5-1.0)
    """
    # Expand style shorthand
    style_prompt = STYLE_PROMPTS.get(style.lower(), style)
    
    # Build full prompt
    prompt = f"{style_prompt} {room_type}, professional architectural photography, photorealistic, magazine quality, natural lighting, high-end finishes"
    
    try:
        # Handle local file paths
        if os.path.isfile(image_url):
            image_input = open(image_url, 'rb')
        else:
            image_input = image_url
            
        output = replicate.run(
            "xlabs-ai/flux-dev-controlnet:9a8db105db745f8b11ad3afe5c8bd892428b2a43ade0b67edc4e0ccd52ff2fda",
            input={
                "control_image": image_input,
                "prompt": prompt,
                "guidance_scale": 3.5,
                "control_strength": preserve,
                "steps": 28,
                "control_type": "depth",
                "output_format": "png",
                "output_quality": 90,
            }
        )
        
        if not output or len(output) == 0:
            raise Exception("No output from model")
        
        # Handle FileOutput objects
        result_url = output[0].url if hasattr(output[0], 'url') else str(output[0])
        
        return {
            "ok": True,
            "url": result_url,
            "method": "controlnet",
            "prompt": prompt,
            "preserve": preserve
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)}


def style_transfer(image_url: str, style: str, strength: float = 0.5) -> dict:
    """
    Lighter style transfer using img2img.
    
    Args:
        image_url: URL to source image
        style: Style description
        strength: How much to change (0.3-0.8)
    """
    style_prompt = STYLE_PROMPTS.get(style.lower(), style)
    prompt = f"{style_prompt}, interior photography, photorealistic"
    
    try:
        output = replicate.run(
            "black-forest-labs/flux-dev",
            input={
                "image": image_url,
                "prompt": prompt,
                "prompt_strength": strength,
                "num_inference_steps": 28,
                "guidance": 3.5,
            }
        )
        
        if not output or len(output) == 0:
            raise Exception("No output from model")
        
        return {
            "ok": True,
            "url": output[0],
            "method": "style_transfer",
            "prompt": prompt,
            "strength": strength
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Pro interior design generation")
    parser.add_argument("--image", required=True, help="URL to source image")
    parser.add_argument("--style", required=True, help="Style description or key")
    parser.add_argument("--room-type", default="interior", help="Room type")
    parser.add_argument("--preserve", type=float, default=0.75, 
                        help="Structure preservation (0.5-1.0)")
    parser.add_argument("--strength", type=float, default=None,
                        help="Style strength for transfer mode (0.3-0.8)")
    parser.add_argument("--mode", choices=["reskin", "transfer"], default="reskin",
                        help="Generation mode")
    
    args = parser.parse_args()
    
    # Check API token
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print(json.dumps({"ok": False, "error": "REPLICATE_API_TOKEN not set"}))
        sys.exit(1)
    
    # Run generation
    if args.mode == "transfer" or args.strength is not None:
        strength = args.strength if args.strength else 0.5
        result = style_transfer(args.image, args.style, strength)
    else:
        result = reskin_room(args.image, args.style, args.room_type, args.preserve)
    
    print(json.dumps(result))
    
    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
