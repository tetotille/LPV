
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QBrush
from PyQt6.QtCore import Qt, QTimer, QRectF

class LedStripWidget(QWidget):
    def __init__(self, led_count=60, parent=None):
        super().__init__(parent)
        self.led_count = led_count
        self.current_led = 0
        self.direction = 1  # 1 for right, -1 for left
        self.setFixedHeight(25)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)  # ~60 FPS for smoother motion

    def animate(self):
        # Move fractional led for smoother movement
        # Increased speed from 0.5 to 1.5
        self.current_led += self.direction * 1.5
        if self.current_led >= self.led_count - 1:
            self.direction = -1
        elif self.current_led <= 0:
            self.direction = 1
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background: Very dark emerald base
        painter.fillRect(self.rect(), QColor(5, 12, 8))
        
        width = self.width()
        height = self.height()
        led_spacing = width / self.led_count
        led_width = led_spacing * 0.7
        
        for i in range(self.led_count):
            x = i * led_spacing + (led_spacing - led_width) / 2
            rect = QRectF(x, height * 0.3, led_width, height * 0.4)
            
            # Distance from current led for "trail" and "glow" effect
            dist = abs(i - self.current_led)
            
            if dist < 0.5:
                # The active LED - Peak Brightness
                color = QColor(50, 255, 180)
                glow_alpha = 180
            elif dist < 5:
                # Trail effect
                intensity = 1.0 - (dist / 5.0)
                color = QColor(int(20 + 30 * intensity), int(80 + 175 * intensity), int(50 + 130 * intensity))
                glow_alpha = int(120 * intensity)
            else:
                # Dim/Off LED
                color = QColor(10, 30, 20)
                glow_alpha = 0

            # Draw Glow (Radial Gradient behind the LED)
            if glow_alpha > 0:
                glow_rect = rect.adjusted(-10, -10, 10, 10)
                gradient = QRadialGradient(rect.center(), 15)
                gradient.setColorAt(0, QColor(0, 255, 150, glow_alpha))
                gradient.setColorAt(1, QColor(0, 255, 150, 0))
                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(glow_rect)

            # Draw LED
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 2, 2)
            
            # Optional: Add a small highlight on the LED
            if dist < 5:
                highlight_rect = QRectF(rect.x() + 1, rect.y() + 1, rect.width() * 0.5, rect.height() * 0.3)
                painter.setBrush(QColor(255, 255, 255, int(100 * (1.0 - dist/5.0))))
                painter.drawRoundedRect(highlight_rect, 1, 1)

