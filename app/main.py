from fastapi import FastAPI, UploadFile, File
import os
import cv2
import threading
import multiprocessing
from app.yolo_detector import detect_objects

app = FastAPI(
    title="API Visual Hackathon",
    description="API desarrollada para el hackathon",
    version="1.0.0"
)

def main():
    cap = cv2.VideoCapture(0)  # 0 es la cámara por defecto

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el frame.")
            break

        # Codifica el frame como imagen JPEG en memoria
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("No se pudo codificar el frame.")
            continue

        image_bytes = buffer.tobytes()
        detections = detect_objects(image_bytes)
        print("Detecciones:", detections)

        # Dibuja las detecciones en el frame
        for det in detections:
            x1, y1, x2, y2 = map(int, det['box'])
            label = f"{det['class']} {det['confidence']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.imshow('YOLO Camera', frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.on_event("startup")
def start_camera_process():
    camera_process = multiprocessing.Process(target=main, daemon=True)
    camera_process.start()

@app.get("/")
async def read_root():
    return {"message": "¡Hola desde FastAPI!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
else:
    print("Cámara abierta correctamente.")
    cap.release()