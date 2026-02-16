import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

def on_click():
    print("Botón presionado")

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Ejemplo QLabel")
window.resize(400, 300)

label = QLabel("Hola Mecatrónica", parent=window)
label.move(120, 100)

button = QPushButton("Presionar", parent=window)
button.move(140, 130)

input = QLineEdit("Hola Mecatrónica", parent=window)
input.move(140, 180)

button.clicked.connect(on_click)

window.show()

app.exec()