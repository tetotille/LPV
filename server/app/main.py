from __future__ import annotations

import os
from pathlib import Path

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.inference import YoloONNXDetector
from app.schemas import DetectionResponse

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = Path(os.getenv("YOLO_ONNX_PATH", BASE_DIR / "onnx_model" / "yolo26s.onnx"))
LABELS_PATH = Path(os.getenv("YOLO_LABELS_PATH", BASE_DIR / "onnx_model" / "labels.txt"))
CONF_THRESHOLD = float(os.getenv("YOLO_CONF", "0.25"))
IOU_THRESHOLD = float(os.getenv("YOLO_IOU", "0.45"))

app = FastAPI(
    title="YOLO ONNX Detection API",
    description="Servidor FastAPI para recibir imagenes y devolver bounding boxes detectados por un modelo YOLO ONNX.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_detector: YoloONNXDetector | None = None


def get_detector() -> YoloONNXDetector:
    global _detector
    if _detector is None:
        _detector = YoloONNXDetector(
            model_path=MODEL_PATH,
            labels_path=LABELS_PATH if LABELS_PATH.exists() else None,
            conf_threshold=CONF_THRESHOLD,
            iou_threshold=IOU_THRESHOLD,
        )
    return _detector


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": str(MODEL_PATH)}


@app.post("/detect", response_model=DetectionResponse)
async def detect(file: UploadFile = File(...)) -> DetectionResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo enviado debe ser una imagen.")

    data = await file.read()
    array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="No se pudo decodificar la imagen.")

    detections = get_detector().predict(image)
    height, width = image.shape[:2]
    return DetectionResponse(image_width=width, image_height=height, detections=[d.__dict__ for d in detections])


def run() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
