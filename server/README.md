# YOLO FastAPI Server

Servidor de ejemplo para recibir una imagen, ejecutar inferencia con `onnx_model/yolo26s.onnx` y devolver detecciones en JSON.

## Instalacion

```bash
cd server
poetry install
```

## Ejecucion

```bash
poetry run yolo-server
```

Tambien puede ejecutarse con:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Variables opcionales:

```bash
set YOLO_CONF=0.25
set YOLO_IOU=0.45
set YOLO_ONNX_PATH=onnx_model/yolo26s.onnx
```

Endpoint principal:

- `POST /detect`: recibe `multipart/form-data` con el campo `file`.
- `GET /health`: verifica que el servidor esta activo.
