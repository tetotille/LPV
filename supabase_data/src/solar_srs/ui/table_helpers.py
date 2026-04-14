from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


COLUMN_ORDER = [
    ("id", "ID"),
    ("date_obs", "Fecha"),
    ("noaa", "NOAA"),
    ("z_class", "Z"),
    ("p_class", "P"),
    ("c_class", "C"),
    ("mcintosh_full", "McIntosh"),
    ("latitude", "Lat"),
    ("longitude", "Lon"),
    ("area", "Área"),
    ("num_spots", "N° spots"),
    ("mag_class", "Mag"),
    ("notes", "Notas"),
]


def populate_table(table: QTableWidget, rows: list[dict[str, Any]]) -> None:
    table.clear()
    table.setColumnCount(len(COLUMN_ORDER))
    table.setHorizontalHeaderLabels([label for _, label in COLUMN_ORDER])
    table.setRowCount(len(rows))

    for i, row in enumerate(rows):
        for j, (key, _) in enumerate(COLUMN_ORDER):
            value = row.get(key)
            text = "" if value is None else str(value)
            table.setItem(i, j, QTableWidgetItem(text))

    table.resizeColumnsToContents()
