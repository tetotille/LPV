# Lenguaje de Programación Visual  
## Ingeniería Mecatrónica

**Semana 9: FastAPI**

---

## Crear entorno virtual con Conda + Jupyter Notebook + Yolov26 (ncnn)

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

---

6. Instalar dependecias para usar yolo26 de ultralytics y generar el ncnn (torch, torchvision, torchaudio,ultralitics, opencv, descargar formato de librerias compatible con CUDA si es detectada)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install ultralytics opencv-python
```

7. Al integrar yolo26 de ultralytics  se descargara el .pt global, luego esto hay que convertirlo a .ncnn para usarlo en pyhton y hacer pruebas con el siguiente script:




