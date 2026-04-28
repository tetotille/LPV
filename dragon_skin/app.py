
from PyQt6.QtWidgets import QApplication
from src.dragon_skin.main_window import MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
