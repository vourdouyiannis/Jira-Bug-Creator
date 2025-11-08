import base64
from io import BytesIO
from PIL import Image


def compress_image(b64_string, max_size_kb=300):
    """
    Compresses a base64 image to reduce size before sending to Gemini.
    Keeps quality decent for UI comparison.
    Returns raw binary bytes.
    """
    try:
        if b64_string.startswith("data:image"):
            b64_string = b64_string.split(",")[1]

        image_data = base64.b64decode(b64_string)
        img = Image.open(BytesIO(image_data)).convert("RGB")

        max_dim = 600
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
