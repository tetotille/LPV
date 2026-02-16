import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QSlider, 
                             QLabel, QFileDialog)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from layout_ledsquare import LEDSquare

class MusicPlayerPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mechatronic Multimedia System - LPV 2026")
        
        # --- Configuración Multimedia ---
        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        
        # Bandera para evitar conflictos durante el "Seek"
        self.is_user_sliding = False
        
        # Conectar señales reales del reproductor
        self.mediaPlayer.positionChanged.connect(self.update_position)
        self.mediaPlayer.durationChanged.connect(self.update_duration)
        
        self.rows, self.cols = 12, 26
        self.init_ui()

    def init_ui(self):
        # --- Menú ---
        menu = self.menuBar()
        file_menu = menu.addMenu("&Archivo")
        
        open_act = QAction("Abrir Canción", self)
        open_act.triggered.connect(self.open_file)
        file_menu.addAction(open_act)
        
        export_act = QAction("Exportar Playlist", self)
        file_menu.addAction(export_act)

        # --- Mosaico (LayoutGrid) ---
        main_layout = QVBoxLayout()
        self.grid = QGridLayout()
        self.grid.setSpacing(2)
        self.matrix = []
        for c in range(self.cols):
            column = [LEDSquare() for _ in range(self.rows)]
            for r, led in enumerate(column):
                self.grid.addWidget(led, r, c)
            self.matrix.append(column)

        # --- Slider de Progreso ---
        progress_layout = QHBoxLayout()
        self.lbl_time = QLabel("00:00 / 00:00")
        self.slider_progress = QSlider(Qt.Orientation.Horizontal)
        self.slider_progress.setRange(0, 0)
        
        # Conexiones mejoradas para el cambio de tiempo (Seek)
        self.slider_progress.sliderPressed.connect(self.on_slider_pressed)
        self.slider_progress.sliderReleased.connect(self.on_slider_released)
        self.slider_progress.sliderMoved.connect(self.on_slider_move)
        
        progress_layout.addWidget(self.lbl_time)
        progress_layout.addWidget(self.slider_progress)

        # --- Controles ---
        controls = QHBoxLayout()
        self.btn_play = QPushButton("PLAY / PAUSE")
        self.btn_play.clicked.connect(self.play_music)
        
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.clicked.connect(self.stop_music)

        # Slider de Volumen (Esquina derecha)
        self.slider_vol = QSlider(Qt.Orientation.Horizontal)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(50)
        self.slider_vol.setFixedWidth(120)
        self.slider_vol.valueChanged.connect(self.set_volume)
        self.audioOutput.setVolume(0.5)

        controls.addWidget(self.btn_play)
        controls.addWidget(self.btn_stop)
        controls.addStretch()
        controls.addWidget(QLabel("VOL"))
        controls.addWidget(self.slider_vol)

        main_layout.addLayout(self.grid)
        main_layout.addLayout(progress_layout)
        main_layout.addLayout(controls)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Timer para animación visual
        self.timer_viz = QTimer()
        self.timer_viz.timeout.connect(self.animate_spectrum)

    # --- Lógica de Control de Tiempo (Seek) ---
    def on_slider_pressed(self):
        self.is_user_sliding = True

    def on_slider_move(self, position):
        # Actualiza el texto mientras arrastras, pero no la posición del audio aún
        self.update_label(position, self.mediaPlayer.duration())

    def on_slider_released(self):
        # Solo cuando sueltas el slider se cambia la posición de la canción
        new_pos = self.slider_progress.value()
        self.mediaPlayer.setPosition(new_pos)
        self.is_user_sliding = False

    # --- Lógica de Multimedia ---
    def open_file(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, "Seleccionar Música", "", "Audio (*.mp3 *.wav *.m4a)")
        if path:
            self.mediaPlayer.setSource(QUrl.fromLocalFile(path))
            self.play_music()

    def play_music(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
            self.timer_viz.stop()
        else:
            self.mediaPlayer.play()
            self.timer_viz.start(80)

    def stop_music(self):
        self.mediaPlayer.stop()
        self.timer_viz.stop()
        self.clear_matrix()
        self.slider_progress.setValue(0)

    def set_volume(self, vol):
        self.audioOutput.setVolume(vol / 100)

    def update_position(self, position):
        # Solo actualiza el slider si el usuario NO lo está moviendo manualmente
        if not self.is_user_sliding:
            self.slider_progress.setValue(position)
            self.update_label(position, self.mediaPlayer.duration())

    def update_duration(self, duration):
        self.slider_progress.setRange(0, duration)
        self.update_label(self.mediaPlayer.position(), duration)

    def update_label(self, current, total):
        curr_m, curr_s = divmod(current // 1000, 60)
        tot_m, tot_s = divmod(total // 1000, 60)
        self.lbl_time.setText(f"{curr_m:02d}:{curr_s:02d} / {tot_m:02d}:{tot_s:02d}")

    def animate_spectrum(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            for col in self.matrix:
                level = random.randint(0, self.rows)
                for r in range(self.rows):
                    # Encendido por columnas (de abajo hacia arriba)
                    col[self.rows-1-r].set_state(r < level)

    def clear_matrix(self):
        for col in self.matrix:
            for led in col: led.set_state(False)


app = QApplication(sys.argv)
window = MusicPlayerPro()
window.show()
sys.exit(app.exec())