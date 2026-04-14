from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow, QTabWidget

from ..services.record_service import RecordService
from ..ui.all_records_widget import AllRecordsWidget
from ..ui.day_records_widget import DayRecordsWidget


class MainWindow(QMainWindow):
    def __init__(self, service: RecordService) -> None:
        super().__init__()
        self.service = service
        self.setWindowTitle("Solar SRS Viewer (Supabase)")
        self.resize(1200, 700)
        self._build_ui()

    def _build_ui(self) -> None:
        tabs = QTabWidget()

        self.all_records_widget = AllRecordsWidget(self.service)
        self.day_records_widget = DayRecordsWidget(self.service)

        tabs.addTab(self.all_records_widget, "Todos los registros")
        tabs.addTab(self.day_records_widget, "Registros por día")

        self.setCentralWidget(tabs)

    def refresh_all(self) -> None:
        self.all_records_widget.refresh()
        self.day_records_widget.refresh_dates()
