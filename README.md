# Lenguaje de Programación Visual

### Ingeniería Mecatrónica

**Semana 2: Diseño UI y Layouts con PyQt6**


**PyQt6** es un framework que permite crear **interfaces gráficas de usuario (GUI)** en Python. Está basado en la biblioteca Qt, que es ampliamente usada en aplicaciones profesionales.

Con PyQt6 puedes crear:

* Ventanas
* Botones
* Etiquetas de texto
* Campos de entrada
* Layouts (diseños)
* Menús
* Eventos interactivos
* Aplicaciones completas con interfaz gráfica

PyQt6 funciona mediante una arquitectura basada en:

* **Widgets** → elementos visuales
* **Layouts** → organización de widgets
* **Signals & Slots** → comunicación entre eventos y funciones
* **Aplicación Qt** → motor principal



**Instalación de dependencias**

Agrega PyQt6 al proyecto usando poetry:

```bash
poetry add pyqt6
```

Verifica la instalación:

```bash
poetry run python -c "import PyQt6"
```


## Estructura básica de una aplicación PyQt6

Toda aplicación PyQt6 necesita estos componentes principales:

1. QApplication → controla la aplicación
2. QWidget o QMainWindow → ventana principal
3. Widgets → elementos visuales
4. Loop de eventos → mantiene la aplicación activa



Ejemplo 1: Ventana básica


```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Mi primera ventana PyQt6")
window.resize(400, 300)

window.show()

app.exec()
```

Ejecutar:

```bash
poetry run python main.py
```

### Widgets básicos

Los widgets son los elementos visuales.

Algunos ejemplos comunes:

* QLabel → texto
* QPushButton → botón
* QLineEdit → campo de texto
* QWidget → contenedor base


Ejemplo 2: Agregar un texto (QLabel)

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Ejemplo QLabel")
window.resize(400, 300)

label = QLabel("Hola Mecatrónica", parent=window)
label.move(120, 130)

window.show()

app.exec()
```

Ejemplo 3: Botón (QPushButton)

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Ejemplo QPushButton")
window.resize(400, 300)

button = QPushButton("Presionar", parent=window)
button.move(140, 130)

window.show()

app.exec()
```


### Signals y Slots (Eventos)

Los botones pueden ejecutar funciones cuando se presionan.

Ejemplo:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

def on_click():
    print("Botón presionado")

app = QApplication(sys.argv)

window = QWidget()
window.resize(400, 300)

button = QPushButton("Click", parent=window)
button.move(150, 130)

button.clicked.connect(on_click)

window.show()

app.exec()
```

### Layouts (Organización automática)

Los layouts permiten organizar widgets automáticamente.

Tipos principales:

* QVBoxLayout → vertical
* QHBoxLayout → horizontal
* QGridLayout → cuadrícula

Ejemplo 4: Layout vertical

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Layout Vertical")

layout = QVBoxLayout()

layout.addWidget(QPushButton("Botón 1"))
layout.addWidget(QPushButton("Botón 2"))
layout.addWidget(QPushButton("Botón 3"))

window.setLayout(layout)

window.show()

app.exec()
```

Ejemplo 5: Layout horizontal

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

app = QApplication(sys.argv)

window = QWidget()

layout = QHBoxLayout()

layout.addWidget(QPushButton("Izquierda"))
layout.addWidget(QPushButton("Centro"))
layout.addWidget(QPushButton("Derecha"))

window.setLayout(layout)

window.show()

app.exec()
```

Ejemplo 6: Campo de texto (QLineEdit)

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton

def mostrar_texto():
    print(input.text())

app = QApplication(sys.argv)

window = QWidget()

layout = QVBoxLayout()

input = QLineEdit()
button = QPushButton("Mostrar texto")

button.clicked.connect(mostrar_texto)

layout.addWidget(input)
layout.addWidget(button)

window.setLayout(layout)

window.show()

app.exec()
```


### Clase principal usando POO (recomendado)

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicación OOP PyQt6")
        self.resize(400, 300)

        layout = QVBoxLayout()

        button = QPushButton("Click")

        button.clicked.connect(self.on_click)

        layout.addWidget(button)

        self.setLayout(layout)

    def on_click(self):
        print("Evento desde clase")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
```

### Widget profesional: QMainWindow

QMainWindow permite agregar:

* barra de menú
* barra de herramientas
* barra de estado
* widget central

Ejemplo básico:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QMainWindow")
        self.resize(400, 300)

        label = QLabel("Contenido central")
        self.setCentralWidget(label)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
```

## Ejercicio recomendado

Crear una aplicación que tenga:

* Una ventana
* Un campo de texto
* Un botón
* Una etiqueta que muestre el texto ingresado


