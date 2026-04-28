
from PyQt6.QtCore import QThread, pyqtSignal
import math
import time

class HexWorker(QThread):
    update_signal = pyqtSignal(list)

    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.mouse = (0, 0)
        self.running = True

    def set_mouse(self, pos):
        self.mouse = pos

    def run(self):
        while self.running:
            heights = []
            mx, my = self.mouse
            for r in range(self.rows):
                row = []
                for c in range(self.cols):
                    # Synchronize with hex_widget.py layout
                    hx = c * 25 * 1.5
                    hy = r * 25 * 1.732
                    if c % 2 == 1:
                        hy += 25 * 1.732 / 2
                    
                    dx = mx - hx
                    dy = my - hy
                    dist = math.sqrt(dx*dx + dy*dy)
                    val = max(0, 20 - dist/15)
                    row.append(val)
                heights.append(row)

            self.update_signal.emit(heights)
            time.sleep(0.03)
