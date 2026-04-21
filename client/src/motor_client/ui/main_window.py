from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from ..config import INITIAL_SPEED_LIMIT, INITIAL_TEMP_LIMIT
from ..logic.app_logic import AppLogic
from .plots import MotorPlots
from .controls import MotorControls

class MotorMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motor Monitor Client")
        self.resize(900, 600)

        self.plots = MotorPlots(INITIAL_SPEED_LIMIT, INITIAL_TEMP_LIMIT)
        self.controls = MotorControls(INITIAL_SPEED_LIMIT, INITIAL_TEMP_LIMIT)
        self.logic = AppLogic(self.plots, self.controls)

        self.controls.speed_limit_spin.valueChanged.connect(lambda v: self.logic.update_limits(v, self.logic.temp_limit))
        self.controls.temp_limit_spin.valueChanged.connect(lambda v: self.logic.update_limits(self.logic.speed_limit, v))
        self.controls.run_btn.clicked.connect(self.run_motor)
        self.controls.stop_btn.clicked.connect(self.stop_motor)

        top = QHBoxLayout()
        top.addWidget(self.controls.status_label)
        top.addWidget(self.controls.speed_label)
        top.addWidget(self.controls.temp_label)
        top.addWidget(self.controls.speed_limit_label)
        top.addWidget(self.controls.speed_limit_spin)
        top.addWidget(self.controls.temp_limit_label)
        top.addWidget(self.controls.temp_limit_spin)
        top.addWidget(self.controls.speed_led_label)
        top.addWidget(self.controls.speed_led)
        top.addWidget(self.controls.temp_led_label)
        top.addWidget(self.controls.temp_led)
        top.addStretch()
        top.addWidget(self.controls.run_btn)
        top.addWidget(self.controls.stop_btn)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.plots.speed_plot)
        layout.addWidget(self.plots.temp_plot)
        self.setLayout(layout)

    def run_motor(self):
        import requests
        from ..config import URL
        try:
            requests.post(f"{URL}/run", timeout=2)
        except Exception:
            self.controls.status_label.setText("Estado: error al iniciar")

    def stop_motor(self):
        import requests
        from ..config import URL
        try:
            requests.post(f"{URL}/stop", timeout=2)
        except Exception:
            self.controls.status_label.setText("Estado: error al detener")