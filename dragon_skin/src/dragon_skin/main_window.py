
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .hex_widget import HexWidget
from .led_strip import LedStripWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emerald Dragon Skin - Reactive Hex Grid")
        self.setGeometry(100, 100, 1200, 900)
        
        # Main layout container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add LED Strip at the top
        self.led_strip = LedStripWidget()
        layout.addWidget(self.led_strip)
        
        # Add Dragon Skin Hex Widget
        self.hex_widget = HexWidget()
        layout.addWidget(self.hex_widget)

