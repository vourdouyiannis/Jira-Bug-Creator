import base64
from io import BytesIO
from PIL import Image


def compress_image(b64_string, max_size_kb=300):
    """
    Compress a base64-encoded image to reduce payload size.

    Resizes image to max 600px dimension and adjusts JPEG quality
    until size is under max_size_kb.

    @param b64_string: str, base64 input image.
    @param max_size_kb: int, max allowed size in KB.

    @return: bytes, compressed binary image data.
    """
    try:
        # Strip off data URI prefix if present
        if b64_string.startswith("data:image"):
            b64_string = b64_string.split(",")[1]

        image_data = base64.b64decode(b64_string)
        img = Image.open(BytesIO(image_data)).convert("RGB")

        max_dim = 600

        # Resize for reasonable quality/runtime tradeoff
        img.thumbnail((max_dim, max_dim))

        buffer = BytesIO()
        quality = 70
        img.save(buffer, format="JPEG", quality=quality)
        size_kb = len(buffer.getvalue()) / 1024

        while size_kb > max_size_kb and quality > 30:
            buffer = BytesIO()
            quality -= 10
            img.save(buffer, format="JPEG", quality=quality)
            size_kb = len(buffer.getvalue()) / 1024

        print(f"📉 Compressed image size: {int(size_kb)}KB")
        return buffer.getvalue()

    except Exception as e:
        print(f"⚠️ Image compression failed: {e}")
        return base64.b64decode(b64_string)
