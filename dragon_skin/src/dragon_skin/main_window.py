
from PyQt6.QtWidgets import QMainWindow
from .hex_widget import HexWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emerald Dragon Skin - Reactive Hex Grid")
        self.setGeometry(100, 100, 1200, 900)
        self.widget = HexWidget()
        self.setCentralWidget(self.widget)
