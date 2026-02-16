from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

# Solo puede haber una instancia de QApplication por 
# aplicacion, su funcion es gestionar todos los recursos
app = QApplication([])

# Ventana de aplicacion, por defecto esta oculta
window = QWidget()
window.show()

# Inciar loop de eventos
app.exec()