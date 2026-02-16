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

        