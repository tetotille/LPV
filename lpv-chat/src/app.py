import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QMessageBox, QInputDialog
)
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor


class WorkerHTTP(QThread):
    """Hilo que realiza una petición HTTP y emite el resultado."""

    resultado = pyqtSignal(object)   # emite el objeto Response
    error     = pyqtSignal(str)      # emite el mensaje de error

    def __init__(self, metodo, url, payload=None, timeout=5):
        super().__init__()
        self.metodo  = metodo    # "GET" o "POST"
        self.url     = url
        self.payload = payload
        self.timeout = timeout

    def run(self):
        try:
            if self.metodo == "GET":
                resp = requests.get(self.url, timeout=self.timeout)
            else:
                resp = requests.post(
                    self.url, json=self.payload, timeout=self.timeout
                )
            self.resultado.emit(resp)
        except Exception as e:
            self.error.emit(str(e))

class WorkerMensajes(QThread):
    """Hilo dedicado a obtener mensajes periódicamente."""

    mensajes_recibidos = pyqtSignal(list)

    def __init__(self, url, intervalo_ms=2000):
        super().__init__()
        self.url         = url
        self.intervalo   = intervalo_ms / 1000  # segundos
        self._corriendo  = True

    def run(self):
        import time
        while self._corriendo:
            try:
                resp = requests.get(self.url, timeout=5)
                if resp.status_code == 200:
                    self.mensajes_recibidos.emit(resp.json())
            except Exception:
                pass
            time.sleep(self.intervalo)

    def detener(self):
        self._corriendo = False


class ChatApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # Si el servidor corre en la MISMA PC → usa 127.0.0.1
        # Si el servidor corre en OTRA PC de la red → pon su IP local
        # Ejemplo red local: self.url_base = "http://172.16.232.224:5000"
        self.url_base = "http://127.0.0.1:5000"

        self.usuario_actual = None
        self._workers = []          # referencias vivas a workers activos

        self.init_ui()

        # Hilo de polling: descarga mensajes cada 2 segundos sin bloquear
        self.worker_mensajes = WorkerMensajes(
            f"{self.url_base}/mensajes", intervalo_ms=2000
        )
        self.worker_mensajes.mensajes_recibidos.connect(self._on_mensajes)
        self.worker_mensajes.start()

    def init_ui(self):

        self.setWindowTitle("Mecatrónica Chat Grupal - Semana 3 (Red Local)")
        self.resize(500, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Menú
        menu_bar = self.menuBar()
        menu_archivo = menu_bar.addMenu("&Menu")

        accion_registro = menu_archivo.addAction("Registrarse")
        accion_registro.triggered.connect(self.registrar_usuario)

        accion_login = menu_archivo.addAction("Iniciar Sesión")
        accion_login.triggered.connect(self.iniciar_sesion)

        menu_archivo.addSeparator()

        accion_salir = menu_archivo.addAction("Salir")
        accion_salir.triggered.connect(self.close)

        # Caja de chat
        self.caja_chat = QTextEdit()
        self.caja_chat.setReadOnly(True)
        self.layout.addWidget(self.caja_chat)

        # Panel inferior
        self.layout_inferior = QHBoxLayout()

        self.input_mensaje = QLineEdit()
        self.input_mensaje.setPlaceholderText("Escribe un mensaje...")
        self.input_mensaje.returnPressed.connect(self.enviar_mensaje)

        self.btn_enviar = QPushButton("Enviar")
        self.btn_enviar.clicked.connect(self.enviar_mensaje)

        self.layout_inferior.addWidget(self.input_mensaje)
        self.layout_inferior.addWidget(self.btn_enviar)
        self.layout.addLayout(self.layout_inferior)

        self.statusBar().showMessage(
            f"Servidor: {self.url_base} | Estado: No conectado"
        )


    def _on_mensajes(self, mensajes):
        self.caja_chat.clear()
        for msg in mensajes:
            nombre = msg['usuario']
            texto  = msg['texto']
            if nombre == self.usuario_actual:
                color = "blue"
            elif nombre == "Sistema":
                color = "red"
            else:
                color = "darkgreen"
            self.caja_chat.append(
                f"<b style='color:{color}'>{nombre}:</b> {texto}"
            )
        self.caja_chat.moveCursor(QTextCursor.MoveOperation.End)

    def _lanzar_worker(self, metodo, url, payload=None,
                        on_resultado=None, on_error=None):
        w = WorkerHTTP(metodo, url, payload)
        if on_resultado:
            w.resultado.connect(on_resultado)
        if on_error:
            w.error.connect(on_error)
        # Limpiamos workers terminados antes de agregar el nuevo
        self._workers = [x for x in self._workers if x.isRunning()]
        self._workers.append(w)
        w.start()

    def registrar_usuario(self):

        nombre, ok1 = QInputDialog.getText(
            self, "Registro", "Crea un nombre de usuario:"
        )
        if not (ok1 and nombre):
            return

        password, ok2 = QInputDialog.getText(
            self, "Registro", "Crea una contraseña:",
            QLineEdit.EchoMode.Password
        )
        if not (ok2 and password):
            return

        payload = {"user": nombre, "password": password}

        def _ok(resp):
            if resp.status_code == 201:
                self.usuario_actual = nombre
                self.statusBar().showMessage(
                    f"Online en {self.url_base}: {self.usuario_actual}"
                )
                QMessageBox.information(self, "Éxito", "Cuenta creada exitosamente.")
            else:
                msg = resp.json().get('error', 'Error al registrar')
                QMessageBox.warning(self, "Error de Registro", msg)

        def _err(e):
            QMessageBox.critical(
                self, "Error", f"No se puede conectar al servidor:\n{e}"
            )

        self._lanzar_worker(
            "POST", f"{self.url_base}/registro", payload,
            on_resultado=_ok, on_error=_err
        )

    def iniciar_sesion(self):

        nombre, ok1 = QInputDialog.getText(
            self, "Inicio de Sesión", "Nombre de usuario:"
        )
        if not (ok1 and nombre):
            return

        password, ok2 = QInputDialog.getText(
            self, "Inicio de Sesión", "Contraseña:",
            QLineEdit.EchoMode.Password
        )
        if not (ok2 and password):
            return

        payload = {"user": nombre, "password": password}

        def _ok(resp):
            if resp.status_code == 200:
                self.usuario_actual = nombre
                self.statusBar().showMessage(
                    f"Online en {self.url_base}: {nombre}"
                )
                QMessageBox.information(self, "Éxito", f"Bienvenido {nombre}")
            else:
                msg = resp.json().get('error', 'Error de autenticación')
                QMessageBox.warning(self, "Error", msg)

        def _err(e):
            QMessageBox.critical(
                self, "Error", f"No se puede conectar al servidor:\n{e}"
            )

        self._lanzar_worker(
            "POST", f"{self.url_base}/login", payload,
            on_resultado=_ok, on_error=_err
        )

    def enviar_mensaje(self):

        if not self.usuario_actual:
            QMessageBox.warning(self, "Error", "Debes iniciar sesión primero.")
            return

        texto = self.input_mensaje.text().strip()
        if not texto:
            return

        self.input_mensaje.clear()   # limpiamos de inmediato (no esperamos)

        payload = {"user": self.usuario_actual, "text": texto}

        def _ok(resp):
            if resp.status_code == 403:
                self.usuario_actual = None
                self.statusBar().showMessage("Sesión expirada")
                QMessageBox.critical(self, "Error", "Sesión no válida")

        def _err(_):
            QMessageBox.critical(self, "Error", "No se puede enviar el mensaje.")

        self._lanzar_worker(
            "POST", f"{self.url_base}/mensajes", payload,
            on_resultado=_ok, on_error=_err
        )

    def closeEvent(self, event):
        # Detener el hilo de polling
        self.worker_mensajes.detener()
        self.worker_mensajes.wait(2000)

        if self.usuario_actual:
            try:
                requests.post(
                    f"{self.url_base}/logout",
                    json={"user": self.usuario_actual},
                    timeout=1
                )
            except Exception:
                pass

        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ChatApp()
    window.show()

    sys.exit(app.exec())