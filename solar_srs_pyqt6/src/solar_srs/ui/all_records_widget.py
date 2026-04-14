from __future__ import annotations

from PyQt6.QtWidgets import QPushButton, QTableWidget, QVBoxLayout, QWidget

from ..services.record_service import RecordService
from ..ui.table_helpers import populate_table


class AllRecordsWidget(QWidget):
    def __init__(self, service: RecordService) -> None:
        super().__init__()
        self.service = service
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.refresh_button = QPushButton("Actualizar tabla")
        self.refresh_button.clicked.connect(self.refresh)
        self.table = QTableWidget()
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.table)

    def refresh(self) -> None:
        rows = self.service.get_all_records()
        populate_table(self.table, rows)
