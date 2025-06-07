from fastapi import FastAPI, UploadFile, File
import os
from app.yolo_detector import detect_objects

app = FastAPI(
    title="API Visual Hackathon",
    description="API desarrollada para el hackathon",
    version="1.0.0"
)

ASSETS_DIR = "assets"
DEFAULT_IMAGE_PATH = os.path.join(ASSETS_DIR, "image2.png")

@app.get("/yolo")
async def yolo_detect():
    if not os.path.exists(DEFAULT_IMAGE_PATH):
        return {"error": "Imagen no encontrada."}

    with open(DEFAULT_IMAGE_PATH, "rb") as f:
        contents = f.read()

    detections = detect_objects(contents)
    return {"filename": os.path.basename(DEFAULT_IMAGE_PATH), "detections": detections}

@app.get("/")
async def read_root():
    return {"message": "¡Hola desde FastAPI!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q} 