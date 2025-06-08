from fastapi import FastAPI, UploadFile, File
import os
import cv2
import threading
import multiprocessing
from app.yolo_detector import detect_objects
import requests
import time

app = FastAPI(
    title="API Visual Hackathon",
    description="API desarrollada para el hackathon",
    version="1.0.0"
)

last_notification_time = 0
detection_counts = {}

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
        # print("Detecciones:", detections)

        # Dibuja las detecciones en el frame
        for det in detections:
            x1, y1, x2, y2 = map(int, det['box'])
            label = f"{det['class']} {det['confidence']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            # if det['confidence'] > 0.5:
            #     push_notfication(det['class'])

        cv2.imshow('YOLO Camera', frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def push_notfication(message):
    global last_notification_time
    now = time.time()
    # Count detections
    detection_counts[message] = detection_counts.get(message, 0) + 1
    if detection_counts[message] >= 3 and now - last_notification_time >= 60:
        url = "https://2024-190-64-83-194.ngrok-free.app/query"
        print(f"Sending notification for {message}")
        data = {
            "document_name": None,
            "text": """OnEn la planta A de BASF, a las 10:00 AM del 07 de junio de 2025, se detectó a un trabajador sin casco de seguridad durante actividades de trasvase de metacrilato de metilo (MMA). Esta sustancia es un líquido incoloro, volátil, altamente inflamable (H225) y con vapores que pueden causar intoxicación por inhalación (H333), irritación respiratoria (H335) y reacciones alérgicas en la piel (H317). El proceso implica conexiones a presión entre cisterna y tanque, y en caso de fallas o fugas, existe riesgo de explosión, incendio y proyección de elementos metálicos. La ausencia de casco expone al trabajador a traumatismos craneales por caída de herramientas, desconexiones accidentales o explosiones. Considerando las medidas establecidas para accidentes químicos y riesgos mecánicos, ¿qué protocolo de seguridad y respuesta inmediata debería haberse activado en este caso? Incluir recomendaciones de confinamiento, evacuación, uso de EPP y control ambiental según las normativas indicadas en los documentos técnicos y de seguridad provistos."""
        }
        requests.post(url, data=data)
        last_notification_time = now
        detection_counts[message] = 0  # Reset count after notification

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