from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
import onnxruntime as ort


@dataclass
class YoloDetection:
    label: str
    class_id: int
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


class YoloONNXDetector:
    """Detector YOLO simple para modelos ONNX exportados desde Ultralytics.

    Soporta salidas frecuentes:
    - [1, 300, 6] con columnas x1, y1, x2, y2, score, class_id.
    - [1, C, N] o [1, N, C] con cajas xywh + scores por clase.
    """

    def __init__(
        self,
        model_path: str | Path,
        labels_path: str | Path | None = None,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
    ) -> None:
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"No se encontro el modelo ONNX: {self.model_path}")

        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        providers = ["CPUExecutionProvider"]
        self.session = ort.InferenceSession(str(self.model_path), providers=providers)
        self.input = self.session.get_inputs()[0]
        self.input_name = self.input.name
        self.input_size = self._read_input_size(self.input.shape)
        self.labels = self._load_labels(labels_path)

    @staticmethod
    def _read_input_size(shape: Iterable[object]) -> tuple[int, int]:
        dims = list(shape)
        # Entrada tipica: [1, 3, H, W]. Si es dinamica se usa 640x640.
        try:
            h = int(dims[2]) if isinstance(dims[2], int) or str(dims[2]).isdigit() else 640
            w = int(dims[3]) if isinstance(dims[3], int) or str(dims[3]).isdigit() else 640
        except Exception:
            h, w = 640, 640
        return w, h

    @staticmethod
    def _load_labels(labels_path: str | Path | None) -> list[str]:
        if labels_path is None:
            return ["object"]
        path = Path(labels_path)
        if not path.exists():
            return ["object"]
        labels = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        return labels or ["object"]

    def predict(self, image_bgr: np.ndarray) -> list[YoloDetection]:
        original_h, original_w = image_bgr.shape[:2]
        input_tensor, scale, pad_left, pad_top = self._preprocess(image_bgr)
        outputs = self.session.run(None, {self.input_name: input_tensor})
        raw = outputs[0]
        boxes, scores, class_ids = self._parse_output(raw, original_w, original_h, scale, pad_left, pad_top)

        keep = self._nms(boxes, scores)
        detections: list[YoloDetection] = []
        for idx in keep:
            x1, y1, x2, y2 = boxes[idx]
            class_id = int(class_ids[idx])
            label = self.labels[class_id] if 0 <= class_id < len(self.labels) else f"class_{class_id}"
            detections.append(
                YoloDetection(
                    label=label,
                    class_id=class_id,
                    confidence=float(scores[idx]),
                    x1=float(max(0, min(original_w, x1))),
                    y1=float(max(0, min(original_h, y1))),
                    x2=float(max(0, min(original_w, x2))),
                    y2=float(max(0, min(original_h, y2))),
                )
            )
        return detections

    def _preprocess(self, image_bgr: np.ndarray) -> tuple[np.ndarray, float, int, int]:
        input_w, input_h = self.input_size
        h, w = image_bgr.shape[:2]
        scale = min(input_w / w, input_h / h)
        new_w, new_h = int(round(w * scale)), int(round(h * scale))
        resized = cv2.resize(image_bgr, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        canvas = np.full((input_h, input_w, 3), 114, dtype=np.uint8)
        pad_left = (input_w - new_w) // 2
        pad_top = (input_h - new_h) // 2
        canvas[pad_top : pad_top + new_h, pad_left : pad_left + new_w] = resized

        rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        tensor = np.transpose(rgb, (2, 0, 1))[None, ...]
        return tensor, scale, pad_left, pad_top

    def _parse_output(
        self,
        output: np.ndarray,
        original_w: int,
        original_h: int,
        scale: float,
        pad_left: int,
        pad_top: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        pred = np.asarray(output)
        pred = np.squeeze(pred)

        if pred.ndim != 2:
            pred = pred.reshape(-1, pred.shape[-1])

        # Caso YOLO tipo [C, N], por ejemplo [84, 8400].
        if pred.shape[0] < pred.shape[1] and pred.shape[0] in range(5, 200):
            pred = pred.T

        boxes: list[list[float]] = []
        scores: list[float] = []
        class_ids: list[int] = []

        if pred.shape[1] == 6:
            # x1,y1,x2,y2,score,class_id. Común en exportaciones con NMS incluido.
            for row in pred:
                score = float(row[4])
                if score < self.conf_threshold:
                    continue
                x1, y1, x2, y2 = map(float, row[:4])
                class_id = int(round(float(row[5])))
                boxes.append(self._undo_letterbox_xyxy(x1, y1, x2, y2, scale, pad_left, pad_top))
                scores.append(score)
                class_ids.append(class_id)
        elif pred.shape[1] > 6:
            # x,y,w,h + class scores. Puede incluir objectness en la columna 4.
            for row in pred:
                class_scores = row[4:]
                class_id = int(np.argmax(class_scores))
                score = float(class_scores[class_id])
                if score < self.conf_threshold:
                    continue
                cx, cy, bw, bh = map(float, row[:4])
                x1, y1 = cx - bw / 2, cy - bh / 2
                x2, y2 = cx + bw / 2, cy + bh / 2
                boxes.append(self._undo_letterbox_xyxy(x1, y1, x2, y2, scale, pad_left, pad_top))
                scores.append(score)
                class_ids.append(class_id)
        else:
            return np.empty((0, 4), dtype=np.float32), np.array([]), np.array([])

        if not boxes:
            return np.empty((0, 4), dtype=np.float32), np.array([]), np.array([])
        return np.asarray(boxes, dtype=np.float32), np.asarray(scores, dtype=np.float32), np.asarray(class_ids, dtype=np.int64)

    @staticmethod
    def _undo_letterbox_xyxy(
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        scale: float,
        pad_left: int,
        pad_top: int,
    ) -> list[float]:
        return [
            (x1 - pad_left) / scale,
            (y1 - pad_top) / scale,
            (x2 - pad_left) / scale,
            (y2 - pad_top) / scale,
        ]

    def _nms(self, boxes: np.ndarray, scores: np.ndarray) -> list[int]:
        if len(boxes) == 0:
            return []
        x1, y1, x2, y2 = boxes.T
        areas = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
        order = scores.argsort()[::-1]
        keep: list[int] = []

        while order.size > 0:
            i = int(order[0])
            keep.append(i)
            if order.size == 1:
                break
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            inter_w = np.maximum(0.0, xx2 - xx1)
            inter_h = np.maximum(0.0, yy2 - yy1)
            inter = inter_w * inter_h
            union = areas[i] + areas[order[1:]] - inter
            iou = inter / np.maximum(union, 1e-6)
            order = order[1:][iou <= self.iou_threshold]
        return keep
