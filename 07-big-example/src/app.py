import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
    QLineEdit, QCheckBox, QComboBox, QSlider, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QStatusBar, QToolBar, QMessageBox
)

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        self.set_color(color)

    def set_color(self, color_name):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color_name))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Control Mecatrónico")
        self.resize(700, 500)

        self.init_ui()

    def init_ui(self):
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        self.btn_debug = QAction(QIcon("bug.png"), "&Modo Debug", self)
        self.btn_debug.setCheckable(True)
        self.btn_debug.triggered.connect(self.toggle_debug)
        toolbar.addAction(self.btn_debug)

        menu = self.menuBar()
        file_menu = menu.addMenu("&Sistema")
        file_menu.addAction(self.btn_debug)
        file_menu.addSeparator()
        file_menu.addAction("Salir", self.close)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        top_layout = QHBoxLayout()
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del sensor...")
        self.selector = QComboBox()
        self.selector.addItems(["Sensor Nivel", "Motor DC", "Servo"])
        
        top_layout.addWidget(QLabel("ID:"))
        top_layout.addWidget(self.input_nombre)
        top_layout.addWidget(self.selector)
        layout.addLayout(top_layout)

        self.grid = QGridLayout()
        self.blocks = [Color("navy"), Color("darkred"), Color("darkgreen"), Color("gold")]
        self.grid.addWidget(self.blocks[0], 0, 0)
        self.grid.addWidget(self.blocks[1], 0, 1)
        self.grid.addWidget(self.blocks[2], 1, 0)
        self.grid.addWidget(self.blocks[3], 1, 1)
        layout.addLayout(self.grid)

        controls = QHBoxLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.update_ui_state)
        
        self.check_active = QCheckBox("Simulación Activa")
        self.check_active.stateChanged.connect(self.update_ui_state)
        
        btn_run = QPushButton("Ejecutar Acción")
        btn_run.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        btn_run.clicked.connect(self.run_process)

        controls.addWidget(QLabel("Potencia:"))
        controls.addWidget(self.slider)
        controls.addWidget(self.check_active)
        controls.addWidget(btn_run)
        layout.addLayout(controls)

    def toggle_debug(self, state):
        msg = "DEBUG ACTIVADO" if state else "Modo Normal"
        self.status.showMessage(msg, 3000)

    def update_ui_state(self):
        val = self.slider.value()
        status_text = f"Nivel: {val}% | {'ACTIVO' if self.check_active.isChecked() else 'STANDBY'}"
        self.status.showMessage(status_text)
        
        if val > 80:
            self.blocks[1].set_color("red")
        else:
            self.blocks[1].set_color("darkred")

    def run_process(self):
        if not self.check_active.isChecked():
            QMessageBox.warning(self, "Error", "Debe activar la simulación primero")
            return

        res = f"Dispositivo: {self.selector.currentText()}\nID: {self.input_nombre.text()}\nPotencia: {self.slider.value()}%"
        QMessageBox.information(self, "Comando Enviado", res)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())