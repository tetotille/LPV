# Modelo YOLOv26 con ONNX

## Crear entorno virtual con Conda + Jupyter Notebook + Yolov26 (ONNX)

Habiendo instalado [Anaconda](https://www.anaconda.com/products/distribution) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html), para crear un entorno virtual se tienen los siguientes pasos:

1. Abrir la terminal o consola de Windows.

2. Crear un entorno virtual con Conda:

```bash
conda create -n lpv2026-1 python=3.12 -y
```

3. Activar el entorno virtual:

```bash
conda activate lpv2026-1
```

4. Instalar dependencias

```bash
conda install numpy matplotlib scipy pandas seaborn scikit-learn ipykernel jinja2

```

5. Registro de entorno en Jupyter

```bash
python -m ipykernel install --user --name lpv2026-1 --display-name "Python (lpv2026-1)"
```


6. Instalar dependencias para usar yolo26 de ultralytics (se descarga la versión de librerías compatible con CUDA si es detectada)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install ultralytics opencv-python onnxruntime-gpu
```
*(Nota: `onnxruntime-gpu` permite aprovechar la tarjeta gráfica NVIDIA para lograr el máximo rendimiento en la inferencia ONNX. Si la GPU no está disponible o no se detecta, el programa seguirá funcionando sin dar errores, pero se ejecutará más lento utilizando únicamente el procesador (CPU)).*

7. Al integrar yolo26 de ultralytics se descargará el `.pt` global, luego esto hay que convertirlo a formato `.onnx`.

Todos estos pasos son realizados en el notebook `yolo26_get_ncnn.ipynb` (se ha mantenido el nombre original del archivo, pero ahora emplea ONNX en lugar de NCNN).
