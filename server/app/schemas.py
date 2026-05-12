from pydantic import BaseModel, Field


class Detection(BaseModel):
    label: str = Field(..., description="Nombre de la clase detectada")
    class_id: int = Field(..., description="Indice numerico de la clase")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confianza de la deteccion")
    x1: float
    y1: float
    x2: float
    y2: float


class DetectionResponse(BaseModel):
    image_width: int
    image_height: int
    detections: list[Detection]
