# Lenguaje de Programación Visual

### Ingeniería Mecatrónica

**Semana 2: Diseño UI y Layouts con PyQt6**


**PyQt** es una libreria de Python para crear aplicaciones GUI con Qt toolkit, fue creada por **Riverbank Computing Limited** desarrollada desde el 1999. La ultima versión basada en Qt6 es **PyQt6** publicada en 2021 con actualizaciones continuas.

PyQt6 puedes crear ventanas, botones, etiquetas de texto, campos de entrada, layouts (diseños), menús, eventos interactivos y aplicaciones completas con interfaz gráfica.

Funciona mediante una arquitectura basada en:
* **App** → controla la aplicación
* **Siganls, Slots and Events** → comunicación entre eventos y funciones
* **Widgets** → elementos visuales
* **Layouts** → organización de widgets
* **Menus** → menús
* **Dialogs** → ventanas emergentes

**Instalación de dependencias**

Agrega PyQt6 al proyecto usando poetry:

```bash
poetry add pyqt6
```

Verifica la instalación:

```bash
poetry run python -c "import PyQt6"
```

## QtApplication

La clase `QApplication` es la encargada de gestionar todos los recursos de la aplicación como el loop permanente de escucha de eventos (pulsar una tecla, mover el mouse, etc.).

Solo debe haber una y solo una instancia de `QApplication` por aplicación.

Ejemplo basico de `app.py`:
```python
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

app = QApplication([])

window = QWidget()
window.show()

app.exec()
```

> Nota: Todos los Qt Wigets pueden ser "ventas", por ejemplo cambiando QWidget por QPushButton("Click") crea un botón, esto es porque todos las clases Qt Widgets son hijas de QWidget.

## Widgets

Un Widgets son elementos visuales de la aplicación, por ejemplo un botón, un campo de texto, una etiqueta, etc.

### 1. Widgets básicos

Algunos ejemplos comunes:

* QLabel → texto
* QPushButton → botón
* QLineEdit → campo de texto
* QWidget → contenedor base

Ejemplo unificado de widgets basicos:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

def on_click():
    print("Botón presionado")

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Ejemplo QLabel")
window.resize(400, 300)

label = QLabel("Hola Mecatrónica", parent=window)
label.move(120, 130)

button = QPushButton("Presionar", parent=window)
button.move(140, 130)

input = QLineEdit("Hola Mecatrónica", parent=window)
input.move(140, 180)

button.clicked.connect(on_click)

window.show()

app.exec()
```

### 2. QMainWindow

QMainWindow es una clase que contiene un set de widgets modificables por herencia como la barra de menú, la barra de herramientas, la barra de estado, entre otros. Además, pueden incorporarse widgets básicos que interactúan dentro de la clase preprogramada modulando asi el codigo entre app.py y demas modulos.

Ejemplo básico

En `myWindow.py`:
```python
from PyQt6.QtWidgets import QMainWindow, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi primera ventana PyQt6")
        
        button = QPushButton("Click")
        self.setCentralWidget(button)
        button.clicked.connect(self.on_click)

    def on_click(self):
        print("Evento de boton presionado")
```

En `app.py`:
```python
from PyQt6.QtWidgets import QApplication
from myWindow import MyWindow
import sys

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()
```

# Siganls, Slots and Events

Los botones pueden ejecutar funciones cuando se presionan.