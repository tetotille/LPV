# Lenguaje de Programación Visual  
## Ingeniería Mecatrónica

**Semana 8: Concurrencia, hilos y `QThread`**

---

## 1. Concurrencia en Interfaces Gráficas (GUI)

En el desarrollo de aplicaciones con **PyQt6**, el hilo principal (*Main Thread*) es el encargado de gestionar la interfaz de usuario y procesar eventos (como mover el mouse o redimensionar la ventana). Si ejecutamos procesos pesados en este hilo, la interfaz dejará de responder.

Para evitar esto, utilizamos **hilos secundarios**. En ingeniería, esto es vital para:
- Procesar datos de sensores en tiempo real.
- Realizar cálculos matemáticos complejos sin bloquear el control.
- Mantener una visualización fluida (FPS constantes).

> **Concepto Clave:** Nunca realices tareas que tomen más de unos pocos milisegundos en el hilo principal. Usa hilos para mantener la fluidez.

---

## 2. Implementación de `QThread` y Señales

PyQt6 proporciona la clase `QThread` para manejar hilos. La comunicación entre el hilo de trabajo (Worker) y la interfaz se realiza mediante **Signals** y **Slots**, lo que garantiza que los datos se transfieran de forma segura entre diferentes contextos de memoria.

### Ventajas de este enfoque:
- **Desacoplamiento**: La lógica matemática (`worker.py`) está separada de la lógica visual (`hex_widget.py`).
- **Fluidez**: El dibujado de la "Piel de Dragón" no se detiene mientras se calculan las distancias.
- **Seguridad**: Las señales de Qt gestionan la sincronización de datos automáticamente.

---

## 3. Proyecto: Emerald Dragon Skin

Este proyecto simula una "piel de dragón" compuesta por hexágonos reactivos. Al pasar el puntero, los hexágonos cercanos detectan la proximidad y activan una transición esmeralda con efectos de inclinación y escala.

### Componentes Principales:
- **HexWorker**: Calcula en segundo plano la distancia del mouse a cada hexágono y determina su "altura" y brillo.
- **HexWidget**: Recibe los datos y utiliza `QPainter` con gradientes radiales para renderizar el efecto premium.
- **Inclined Geometry**: Los hexágonos se deforman dinámicamente para simular una elevación 3D hacia el usuario.

---

## 4. Estructura del Código (Concurrencia)

A continuación se muestra el bloque de código fundamental que permite la comunicación asíncrona entre el motor de cálculo y la visualización:

```python
# src/dragon_skin/worker.py
from PyQt6.QtCore import QThread, pyqtSignal
import math, time

class HexWorker(QThread):
    # Definición de la señal que transportará la matriz de datos
    update_signal = pyqtSignal(list)

    def run(self):
        while self.running:
            # 1. Obtener posición del mouse
            # 2. Calcular distancias para cada hexágono (Matriz R x C)
            # 3. Generar valores de intensidad
            heights = self.process_logic()
            
            # 4. Emitir señal con los nuevos datos
            self.update_signal.emit(heights)
            
            # Control de frecuencia (aprox 30 FPS)
            time.sleep(0.03)

# src/dragon_skin/hex_widget.py
class HexWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Instanciar e iniciar el hilo secundario
        self.worker = HexWorker(self.rows, self.cols)
        
        # CONEXIÓN CRÍTICA: Unir la señal del Worker con el Slot de la UI
        self.worker.update_signal.connect(self.update_heights)
        self.worker.start()

    def update_heights(self, heights):
        self.heights = heights
        self.update() # Provoca la ejecución de paintEvent()
```

---

## 5. Ejecución del Proyecto

Asegúrate de tener instaladas las dependencias mediante **Poetry**:

```bash
poetry install
poetry run python app.py
```
