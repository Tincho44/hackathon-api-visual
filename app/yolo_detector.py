# app/yolo_detector.py

import torch
# 1) Salvamos el torch.load original
_torch_load = torch.load

# 2) Reemplazamos torch.load para forzar weights_only=False
def _load_force_weights_false(f, *args, **kwargs):
    return _torch_load(f, weights_only=False, *args, **kwargs)

torch.load = _load_force_weights_false


from ultralytics import YOLO
from typing import List, Dict
from PIL import Image
import io

# 3) Aquí cargamos el modelo con el monkey-patch activo
model = YOLO('yolov8s')


def detect_objects(image_bytes: bytes) -> List[Dict]:
    """
    Recibe una imagen en bytes y retorna una lista de objetos detectados.
    Cada dict contiene:
      - class: nombre de la clase detectada
      - confidence: confianza (float)
      - box: [x1, y1, x2, y2]
    """
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    results = model(image)

    detections: List[Dict] = []
    for result in results:
        for box in result.boxes:
            detections.append({
                'class': model.names[int(box.cls)],
                'confidence': float(box.conf),
                'box': [float(c) for c in box.xyxy[0].tolist()]
            })
    return detections
