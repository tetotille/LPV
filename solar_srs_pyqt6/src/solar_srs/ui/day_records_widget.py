from __future__ import annotations

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

from ..services.record_service import RecordService
from ..ui.table_helpers import populate_table


class DayRecordsWidget(QWidget):
    def __init__(self, service: RecordService) -> None:
        super().__init__()
        self.service = service
        self._build_ui()
        self.refresh_dates()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        top.addWidget(QLabel("Selecciona una fecha:"))
        self.date_combo = QComboBox()
        self.load_button = QPushButton("Cargar")
        self.load_button.clicked.connect(self.load_selected_date)
        top.addWidget(self.date_combo)
        top.addWidget(self.load_button)
        top.addStretch()

        self.table = QTableWidget()
        layout.addLayout(top)
        layout.addWidget(self.table)

    def refresh_dates(self) -> None:
        current = self.date_combo.currentText()
        self.date_combo.clear()
        dates = self.service.list_dates()
        self.date_combo.addItems(dates)
        if current and current in dates:
            self.date_combo.setCurrentText(current)
        if self.date_combo.count() > 0:
            self.load_selected_date()
        else:
            populate_table(self.table, [])

    def load_selected_date(self) -> None:
        date_obs = self.date_combo.currentText().strip()
        rows = self.service.get_records_by_date(date_obs) if date_obs else []
        populate_table(self.table, rows)
