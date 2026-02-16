import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QComboBox, QSlider, QMessageBox

def mostrar_mensaje():
    msg = QMessageBox(window)
    msg.setText("Interacción detectada")
    msg.exec()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Ejemplo Widgets")
window.resize(400, 450)

# QLabel
label = QLabel("Hola Mecatrónica", parent=window)
label.move(30, 20)

# QPushButton
button = QPushButton("Presionar", parent=window)
button.move(30, 60)
button.clicked.connect(mostrar_mensaje)

# QLineEdit
input_field = QLineEdit("Hola Mecatrónica", parent=window)
input_field.move(30, 110)
input_field.returnPressed.connect(mostrar_mensaje)

# QCheckBox
check = QCheckBox("Checkbox", parent=window)
check.move(30, 160)
check.clicked.connect(mostrar_mensaje)

# QComboBox
combo = QComboBox(parent=window)
combo.addItems(["Opción 1", "Opción 2", "Opción 3"])
combo.move(30, 210)
combo.activated.connect(mostrar_mensaje)

# QSlider
slider = QSlider(parent=window)
slider.setRange(0, 100)
slider.move(30, 260)
slider.sliderReleased.connect(mostrar_mensaje)

window.show()

sys.exit(app.exec())