from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget

class LEDSquare(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setFixedSize(22, 22)
        self.set_state(False)

    def set_state(self, active):
        # Color verde brillante para activo, gris oscuro para inactivo
        color = QColor(0, 255, 150) if active else QColor(30, 30, 30)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)