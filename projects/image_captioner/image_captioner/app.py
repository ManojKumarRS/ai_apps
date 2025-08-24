import base64
from io import BytesIO
from fastapi import FastAPI, Body
from PIL import Image

api = FastAPI(title="Image Captioner")

@api.get("/health")
def health():
    return {"status": "ok"}

@api.post("/caption")
def caption(image_b64: str = Body(..., embed=True)):
    try:
        img = Image.open(BytesIO(base64.b64decode(image_b64)))
        w, h = img.size
        return {"caption": f"Image {w}x{h}"}
    except Exception:
        return {"error": "Invalid image"}

