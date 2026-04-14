from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from .db.database import DatabaseManager
from .ui.main_window import MainWindow
from .services.record_service import RecordService


def main() -> int:
    app = QApplication(sys.argv)
    db = DatabaseManager()
    service = RecordService(db)
    window = MainWindow(service)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
