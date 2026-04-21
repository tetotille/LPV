from collections import deque
from PyQt6.QtCore import QTimer
from ..config import DATA_POINTS, UPDATE_INTERVAL
from ..data.updater import UpdateThread
from ..ui.plots import MotorPlots
from ..ui.controls import MotorControls

class AppLogic:
    def __init__(self, plots, controls):
        self.plots = plots
        self.controls = controls
        self.speed_values = deque(maxlen=DATA_POINTS)
        self.temp_values = deque(maxlen=DATA_POINTS)
        self.x_values = list(range(DATA_POINTS))
        self.alert_active = False
        self.speed_limit = 3200.0
        self.temp_limit = 80.0

        self.timer = QTimer()
        self.timer.timeout.connect(self.start_update)
        self.timer.start(UPDATE_INTERVAL)

    def update_limits(self, speed_limit, temp_limit):
        self.speed_limit = speed_limit
        self.temp_limit = temp_limit
        self.plots.update_limits(speed_limit, temp_limit)

    def start_update(self):
        self.update_thread = UpdateThread()
        self.update_thread.data_fetched.connect(self.update_ui)
        self.update_thread.start()

    def update_ui(self, data):
        if not data:
            self.controls.status_label.setText("Estado: sin conexión con el servidor")
            return

        speed = float(data["speed"])
        temp = float(data["temp"])
        running = bool(data["running"])
        over = bool(data["over"])

        self.controls.status_label.setText("Estado: RUNNING" if running else "Estado: STOPPED")
        self.controls.speed_label.setText(f"Velocidad: {speed:.1f} RPM")
        self.controls.temp_label.setText(f"Temperatura: {temp:.1f} °C")

        self.speed_values.append(speed)
        self.temp_values.append(temp)

        self.plots.update_data(self.x_values, list(self.speed_values), list(self.temp_values))

        if speed > self.speed_limit:
            self.controls.start_speed_led_blink()
        else:
            self.controls.stop_speed_led_blink()

        if temp > self.temp_limit:
            self.controls.start_temp_led_blink()
        else:
            self.controls.stop_temp_led_blink()

        if over and not self.alert_active:
            self.alert_active = True
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                None,  # No parent for now
                "Alerta de velocidad",
                "La velocidad excedió el límite. Detenga el motor."
            )
        elif not over:
            self.alert_active = False