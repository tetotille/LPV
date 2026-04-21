import requests
from PyQt6.QtCore import QThread, pyqtSignal

class UpdateThread(QThread):
    data_fetched = pyqtSignal(dict)

    def run(self):
        try:
            data = requests.get("http://127.0.0.1:8443/status", timeout=1).json()
            self.data_fetched.emit(data)
        except Exception:
            self.data_fetched.emit({})