"""
Image Operations Plugin
Resize, crop, convert, and analyze images.
"""
import logging
import io
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.image_ops")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def image_resize_cmd(file_path: str = "", width: int = 0, height: int = 0, output: str = "") -> Dict:
    if not PIL_AVAILABLE:
        raise ImportError("Pillow not installed. Run: pip install pillow")
    img = Image.open(file_path)
    resized = img.resize((width, height), Image.Resampling.LANCZOS)
    out = output or file_path.replace(".png", "_resized.png").replace(".jpg", "_resized.jpg")
    resized.save(out)
    return {"status": "resized", "input": file_path, "output": out, "size": [width, height]}


def image_crop_cmd(file_path: str = "", left: int = 0, top: int = 0, right: int = 0, bottom: int = 0,
                   output: str = "") -> Dict:
    if not PIL_AVAILABLE:
        raise ImportError("Pillow not installed. Run: pip install pillow")
    img = Image.open(file_path)
    cropped = img.crop((left, top, right, bottom))
    out = output or file_path.replace(".png", "_cropped.png").replace(".jpg", "_cropped.jpg")
    cropped.save(out)
    return {"status": "cropped", "output": out, "box": [left, top, right, bottom]}


def image_convert_cmd(file_path: str = "", format: str = "PNG", output: str = "") -> Dict:
    if not PIL_AVAILABLE:
        raise ImportError("Pillow not installed. Run: pip install pillow")
    img = Image.open(file_path)
    out = output or file_path.rsplit(".", 1)[0] + "." + format.lower()
    img.save(out, format=format.upper())
    return {"status": "converted", "output": out, "format": format}


def image_thumbnail_cmd(file_path: str = "", max_size: int = 128, output: str = "") -> Dict:
    if not PIL_AVAILABLE:
        raise ImportError("Pillow not installed. Run: pip install pillow")
    img = Image.open(file_path)
    img.thumbnail((max_size, max_size))
    out = output or file_path.replace(".png", "_thumb.png").replace(".jpg", "_thumb.jpg")
    img.save(out)
    return {"status": "thumbnail", "output": out, "size": list(img.size)}


def image_get_info_cmd(file_path: str = "") -> Dict:
    if not PIL_AVAILABLE:
        raise ImportError("Pillow not installed. Run: pip install pillow")
    img = Image.open(file_path)
    return {
        "format": img.format, "mode": img.mode, "size": list(img.size),
        "width": img.width, "height": img.height,
    }


def image_rotate_cmd(file_path: str = "", degrees: int = 90, output: str = "") -> Dict:
    if not PIL_AVAILABLE:
        raise ImportError("Pillow not installed. Run: pip install pillow")
    img = Image.open(file_path)
    rotated = img.rotate(degrees, expand=True)
    out = output or file_path.replace(".png", "_rotated.png").replace(".jpg", "_rotated.jpg")
    rotated.save(out)
    return {"status": "rotated", "output": out, "degrees": degrees}


def image_grayscale_cmd(file_path: str = "", output: str = "") -> Dict:
    if not PIL_AVAILABLE:
        raise ImportError("Pillow not installed. Run: pip install pillow")
    img = Image.open(file_path).convert("L")
    out = output or file_path.replace(".png", "_gray.png").replace(".jpg", "_gray.jpg")
    img.save(out)
    return {"status": "grayscale", "output": out}


def register(plugin):
    plugin.register_command("resize", image_resize_cmd)
    plugin.register_command("crop", image_crop_cmd)
    plugin.register_command("convert", image_convert_cmd)
    plugin.register_command("thumbnail", image_thumbnail_cmd)
    plugin.register_command("get_info", image_get_info_cmd)
    plugin.register_command("rotate", image_rotate_cmd)
    plugin.register_command("grayscale", image_grayscale_cmd)


PLUGIN_METADATA = {
    "name": "image_ops", "version": "1.0.0",
    "description": "Image resize, crop, convert, thumbnail, rotate, and analyze",
    "author": "Mito Team", "license": "MIT",
    "tags": ["image", "resize", "crop", "convert", "utilities"],
    "dependencies": ["pillow"], "permissions": ["read_files", "write_files"],
    "min_mito_version": "1.0.1",
}

image_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
