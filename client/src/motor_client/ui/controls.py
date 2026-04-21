from PyQt6.QtWidgets import QLabel, QPushButton, QDoubleSpinBox
from PyQt6.QtCore import QTimer

class MotorControls:
    def __init__(self, speed_limit, temp_limit):
        self.status_label = QLabel("Estado: desconectado")
        self.speed_label = QLabel("Velocidad: -- RPM")
        self.temp_label = QLabel("Temperatura: -- °C")

        self.speed_limit_label = QLabel("Límite Velocidad:")
        self.speed_limit_spin = QDoubleSpinBox()
        self.speed_limit_spin.setRange(0, 5000)
        self.speed_limit_spin.setValue(speed_limit)
        self.speed_limit_spin.setSuffix(" RPM")

        self.temp_limit_label = QLabel("Límite Temperatura:")
        self.temp_limit_spin = QDoubleSpinBox()
        self.temp_limit_spin.setRange(0, 150)
        self.temp_limit_spin.setValue(temp_limit)
        self.temp_limit_spin.setSuffix(" °C")

        # LEDs
        self.speed_led = QLabel()
        self.speed_led.setFixedSize(20, 20)
        self.speed_led.setStyleSheet("background-color: gray; border-radius: 10px;")
        self.speed_led_label = QLabel("LED Velocidad")

        self.temp_led = QLabel()
        self.temp_led.setFixedSize(20, 20)
        self.temp_led.setStyleSheet("background-color: gray; border-radius: 10px;")
        self.temp_led_label = QLabel("LED Temperatura")

        self.speed_led_timer = QTimer()
        self.speed_led_timer.timeout.connect(self.toggle_speed_led)
        self.speed_led_on = False

        self.temp_led_timer = QTimer()
        self.temp_led_timer.timeout.connect(self.toggle_temp_led)
        self.temp_led_on = False

        self.run_btn = QPushButton("Run")
        self.stop_btn = QPushButton("Stop")

    def toggle_speed_led(self):
        self.speed_led_on = not self.speed_led_on
        color = "red" if self.speed_led_on else "gray"
        self.speed_led.setStyleSheet(f"background-color: {color}; border-radius: 10px;")

    def toggle_temp_led(self):
        self.temp_led_on = not self.temp_led_on
        color = "red" if self.temp_led_on else "gray"
        self.temp_led.setStyleSheet(f"background-color: {color}; border-radius: 10px;")

    def start_speed_led_blink(self):
        if not self.speed_led_timer.isActive():
            self.speed_led_timer.start(500)

    def stop_speed_led_blink(self):
        self.speed_led_timer.stop()
        self.speed_led.setStyleSheet("background-color: gray; border-radius: 10px;")

    def start_temp_led_blink(self):
        if not self.temp_led_timer.isActive():
            self.temp_led_timer.start(500)

    def stop_temp_led_blink(self):
        self.temp_led_timer.stop()
        self.temp_led.setStyleSheet("background-color: gray; border-radius: 10px;")