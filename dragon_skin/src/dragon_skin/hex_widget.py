
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPolygonF, QRadialGradient, QBrush
from PyQt6.QtCore import Qt, QPointF
from .worker import HexWorker
import math

class HexWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.hex_size = 25
        self.cols = 35
        self.rows = 25
        self.heights = [[0]*self.cols for _ in range(self.rows)]

        self.worker = HexWorker(self.rows, self.cols)
        self.worker.update_signal.connect(self.update_heights)
        self.worker.start()

        self.mouse_pos = (0, 0)

    def mouseMoveEvent(self, event):
        self.mouse_pos = (event.position().x(), event.position().y())
        self.worker.set_mouse(self.mouse_pos)

    def update_heights(self, heights):
        self.heights = heights
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background: Deep dark emerald/black
        painter.fillRect(self.rect(), QColor(5, 15, 10))

        for r in range(self.rows):
            for c in range(self.cols):
                # Horizontal spacing: size * 1.5
                # Vertical spacing: size * sqrt(3)
                x = c * self.hex_size * 1.5
                y = r * self.hex_size * 1.732 # math.sqrt(3) approx
                if c % 2 == 1:
                    y += self.hex_size * 1.732 / 2

                h = self.heights[r][c]
                
                # Dynamic Emerald Gradient
                # h varies from 0 to 20
                # Base color: Dark Emerald
                # Highlight color: Bright Emerald / Mint
                intensity = h / 20.0
                
                center_color = QColor(
                    int(10 + 100 * intensity), 
                    int(80 + 175 * intensity), 
                    int(50 + 150 * intensity)
                )
                edge_color = QColor(
                    int(5 + 20 * intensity), 
                    int(40 + 40 * intensity), 
                    int(25 + 25 * intensity)
                )

                gradient = QRadialGradient(QPointF(x, y), self.hex_size * (1.0 + intensity * 0.5))
                gradient.setColorAt(0, center_color)
                gradient.setColorAt(1, edge_color)

                painter.setBrush(QBrush(gradient))
                painter.setPen(Qt.PenStyle.NoPen)

                # Hexagon size and inclination effect
                # We can simulate "inclination" by slightly offsetting the points based on height
                current_size = self.hex_size * (0.8 + intensity * 0.4)
                hexagon = self.create_hexagon(x, y, current_size, intensity)
                painter.drawPolygon(hexagon)

    def create_hexagon(self, x, y, size, intensity):
        points = []
        # Inclination effect: shift points based on intensity to simulate a 3D lift
        tilt_x = intensity * 5
        tilt_y = intensity * -5
        
        for i in range(6):
            angle = math.pi / 3 * i
            # Add a bit of "3D" perspective by scaling the y coordinates slightly differently
            px = x + size * math.cos(angle) + tilt_x
            py = y + size * math.sin(angle) * (1.0 - intensity * 0.1) + tilt_y
            points.append(QPointF(px, py))
        return QPolygonF(points)
