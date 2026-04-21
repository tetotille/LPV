import sys
from PyQt6.QtWidgets import QApplication
from .ui.main_window import MotorMonitor

def main():
    app = QApplication(sys.argv)
    window = MotorMonitor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
