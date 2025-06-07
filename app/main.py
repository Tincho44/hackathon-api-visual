from fastapi import FastAPI, UploadFile, File
import os
from app.yolo_detector import detect_objects

app = FastAPI(
    title="API Visual Hackathon",
    description="API desarrollada para el hackathon",
    version="1.0.0"
)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

@app.post("/yolo")
async def yolo_detect(file: UploadFile = File(...)):
    # Guardar la imagen en assets
    file_location = os.path.join(ASSETS_DIR, file.filename)
    contents = await file.read()
    with open(file_location, "wb") as f:
        f.write(contents)
    # Procesar la imagen
    detections = detect_objects(contents)
    return {"filename": file.filename, "detections": detections}

@app.get("/")
async def read_root():
    return {"message": "¡Hola desde FastAPI!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q} 