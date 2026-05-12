# YOLO PyQt6 Client

Interfaz grafica de ejemplo para capturar una imagen desde webcam, enviarla al servidor FastAPI y visualizar los bounding boxes recibidos.

## Instalacion

```bash
cd client
poetry install
```

## Ejecucion

```bash
poetry run yolo-client
```

Flujo de uso:

1. Ejecute el servidor en otra terminal.
2. Abra el cliente.
3. Presione `Tomar foto` o `Abrir imagen`.
4. Presione `Enviar al servidor`.
5. Revise los bounding boxes dibujados sobre la imagen.
