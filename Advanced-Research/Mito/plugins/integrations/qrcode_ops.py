"""
QR Code Plugin
Generate QR codes, barcodes, and read codes from images.
"""
import logging
import io
import base64
from typing import Any, Dict

logger = logging.getLogger("mito.plugins.qrcode_ops")

try:
    import qrcode
    import qrcode.image.svg
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


def qrcode_generate_cmd(data: str = "", output: str = "", format: str = "PNG", size: int = 10) -> Dict:
    if not QR_AVAILABLE:
        raise ImportError("qrcode not installed. Run: pip install qrcode[pil]")
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgImage if format == "SVG" else None)
    if format == "SVG":
        with open(output or "qrcode.svg", "w") as f:
            f.write(img.to_string())
    else:
        img.save(output or "qrcode.png")
    return {"status": "generated", "data": data, "output": output or "qrcode.png", "format": format}


def qrcode_generate_base64_cmd(data: str = "", format: str = "PNG") -> Dict:
    if not QR_AVAILABLE:
        raise ImportError("qrcode not installed. Run: pip install qrcode[pil]")
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format=format.upper())
    b64 = base64.b64encode(buf.getvalue()).decode()
    return {"format": format, "data": f"data:image/{format.lower()};base64,{b64}"}


def qrcode_read_cmd(file_path: str = "") -> Dict:
    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
        img = Image.open(file_path)
        decoded = decode(img)
        return {"codes": [{"type": d.type, "data": d.data.decode()} for d in decoded], "count": len(decoded)}
    except ImportError:
        return {"error": "Install pillow and pyzbar to read QR codes: pip install pillow pyzbar"}


def qrcode_batch_cmd(data_list: str = "", output_dir: str = "qrcodes/") -> Dict:
    import os
    if not QR_AVAILABLE:
        raise ImportError("qrcode not installed. Run: pip install qrcode[pil]")
    os.makedirs(output_dir, exist_ok=True)
    items = [d.strip() for d in data_list.split(",")]
    for i, item in enumerate(items):
        img = qrcode.make(item)
        img.save(f"{output_dir}/qr_{i}.png")
    return {"status": "batch_generated", "count": len(items), "dir": output_dir}


def register(plugin):
    plugin.register_command("generate", qrcode_generate_cmd)
    plugin.register_command("generate_base64", qrcode_generate_base64_cmd)
    plugin.register_command("read", qrcode_read_cmd)
    plugin.register_command("batch", qrcode_batch_cmd)


PLUGIN_METADATA = {
    "name": "qrcode_ops", "version": "1.0.0",
    "description": "QR code and barcode generation and reading",
    "author": "Mito Team", "license": "MIT",
    "tags": ["qrcode", "barcode", "generation", "utilities"],
    "dependencies": ["qrcode[pil]"], "permissions": ["write_files"],
    "min_mito_version": "1.0.1",
}

qrcode_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
