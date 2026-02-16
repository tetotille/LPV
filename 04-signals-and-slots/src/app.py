import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)

        # Conectamos el slot al signal
        button.clicked.connect(self.the_button_was_clicked)
        self.setCentralWidget(button)

    # Este es el slot
    def the_button_was_clicked(self, checked):
        print(f"The button was clicked! Checked: {checked}")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

