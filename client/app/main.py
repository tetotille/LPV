from __future__ import annotations

import os
import sys
from pathlib import Path

# Fix para el plugin de Conda (evita el error 'Could not find the Qt platform plugin "windows"')
if "CONDA_PREFIX" in os.environ:
    qt_plugins = os.path.join(os.environ["CONDA_PREFIX"], "Library", "plugins")
    if os.path.exists(qt_plugins) and "QT_PLUGIN_PATH" not in os.environ:
        os.environ["QT_PLUGIN_PATH"] = qt_plugins

import cv2
import numpy as np
import requests
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DetectionClient(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Cliente YOLO ONNX - FastAPI")
        self.resize(1050, 760)

        self.camera = cv2.VideoCapture(0)
        self.current_frame: np.ndarray | None = None
        self.last_result_frame: np.ndarray | None = None

        self.image_label = QLabel("Vista de camara")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(900, 600)
        self.image_label.setStyleSheet("border: 1px solid #999; background: #222; color: white;")

        self.server_input = QLineEdit("http://127.0.0.1:8000/detect")
        self.status_label = QLabel("Listo. Inicie el servidor y tome una foto.")

        self.capture_button = QPushButton("Tomar foto")
        self.send_button = QPushButton("Enviar al servidor")
        self.open_button = QPushButton("Abrir imagen")
        self.save_button = QPushButton("Guardar resultado")

        self.capture_button.clicked.connect(self.capture_photo)
        self.send_button.clicked.connect(self.send_to_server)
        self.open_button.clicked.connect(self.open_image)
        self.save_button.clicked.connect(self.save_result)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Endpoint:"))
        controls.addWidget(self.server_input, stretch=1)

        buttons = QHBoxLayout()
        buttons.addWidget(self.capture_button)
        buttons.addWidget(self.send_button)
        buttons.addWidget(self.open_button)
        buttons.addWidget(self.save_button)

        root = QVBoxLayout()
        root.addLayout(controls)
        root.addWidget(self.image_label, stretch=1)
        root.addLayout(buttons)
        root.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(30)

    def update_camera(self) -> None:
        if self.camera.isOpened() and self.last_result_frame is None:
            ok, frame = self.camera.read()
            if ok:
                self.current_frame = frame
                self.show_image(frame)

    def capture_photo(self) -> None:
        if self.current_frame is None:
            QMessageBox.warning(self, "Camara", "No se pudo obtener una imagen de la camara.")
            return
        self.last_result_frame = self.current_frame.copy()
        self.show_image(self.last_result_frame)
        self.status_label.setText("Foto capturada. Puede enviarla al servidor.")

    def open_image(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen",
            "",
            "Imagenes (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)",
        )
        if not file_name:
            return
        image = cv2.imread(file_name)
        if image is None:
            QMessageBox.warning(self, "Imagen", "No se pudo abrir la imagen seleccionada.")
            return
        self.current_frame = image
        self.last_result_frame = image.copy()
        self.show_image(self.last_result_frame)
        self.status_label.setText(f"Imagen cargada: {file_name}")

    def send_to_server(self) -> None:
        frame = self.last_result_frame if self.last_result_frame is not None else self.current_frame
        if frame is None:
            QMessageBox.warning(self, "Imagen", "Primero tome una foto o abra una imagen.")
            return

        endpoint = self.server_input.text().strip()
        ok, encoded = cv2.imencode(".jpg", frame)
        if not ok:
            QMessageBox.warning(self, "Imagen", "No se pudo codificar la imagen.")
            return

        self.status_label.setText("Enviando imagen al servidor...")
        QApplication.processEvents()

        try:
            response = requests.post(
                endpoint,
                files={"file": ("capture.jpg", encoded.tobytes(), "image/jpeg")},
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            QMessageBox.critical(self, "Servidor", f"Error al consultar el servidor:\n{exc}")
            self.status_label.setText("Error al enviar imagen.")
            return

        detections = payload.get("detections", [])
        result = self.draw_detections(frame.copy(), detections)
        self.last_result_frame = result
        self.show_image(result)
        self.status_label.setText(f"Detecciones recibidas: {len(detections)}")

    def draw_detections(self, image: np.ndarray, detections: list[dict]) -> np.ndarray:
        for det in detections:
            x1, y1, x2, y2 = [int(round(float(det[k]))) for k in ("x1", "y1", "x2", "y2")]
            label = str(det.get("label", "object"))
            conf = float(det.get("confidence", 0.0))
            text = f"{label} {conf:.2f}"

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text_y = max(20, y1 - 8)
            cv2.putText(image, text, (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return image

    def show_image(self, image_bgr: np.ndarray) -> None:
        rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimage = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888).copy()
        pixmap = QPixmap.fromImage(qimage).scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setPixmap(pixmap)

    def save_result(self) -> None:
        if self.last_result_frame is None:
            QMessageBox.information(self, "Guardar", "No hay resultado para guardar.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar resultado", "resultado.jpg", "JPEG (*.jpg);;PNG (*.png)")
        if file_name:
            cv2.imwrite(file_name, self.last_result_frame)
            self.status_label.setText(f"Resultado guardado en: {file_name}")

    def closeEvent(self, event) -> None:  # noqa: N802 - API PyQt
        if self.camera.isOpened():
            self.camera.release()
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = DetectionClient()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
