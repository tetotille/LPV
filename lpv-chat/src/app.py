import sys
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QMessageBox, QInputDialog)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QTextCursor

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.url_base = "http://127.0.0.1:5000"
        self.usuario_actual = None
        
        self.init_ui()
        
        # Timer para actualizar mensajes cada 2 segundos (Protocolo GET)
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_chat)
        self.timer.start(2000)

    def init_ui(self):
        self.setWindowTitle("Mecatrónica Chat Grupal - Semana 3")
        self.resize(500, 600)

        # Widget Principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Barra de Menú
        menu_bar = self.menuBar()
        menu_archivo = menu_bar.addMenu("&Menu")
        
        accion_registro = menu_archivo.addAction("Registrarse")
        accion_registro.triggered.connect(self.registrar_usuario)

        accion_login = menu_archivo.addAction("Iniciar Sesión")
        accion_login.triggered.connect(self.iniciar_sesion)
        
        menu_archivo.addSeparator()
        accion_salir = menu_archivo.addAction("Salir")
        accion_salir.triggered.connect(self.close)

        # Panel de visualización de Chat (GET)
        self.caja_chat = QTextEdit()
        self.caja_chat.setReadOnly(True)
        self.layout.addWidget(self.caja_chat)

        # Panel de Control Inferior
        self.layout_inferior = QHBoxLayout()
        
        self.input_mensaje = QLineEdit()
        self.input_mensaje.setPlaceholderText("Escribe un mensaje...")
        self.input_mensaje.returnPressed.connect(self.enviar_mensaje)
        
        self.btn_enviar = QPushButton("Enviar")
        self.btn_enviar.clicked.connect(self.enviar_mensaje)
        
        self.layout_inferior.addWidget(self.input_mensaje)
        self.layout_inferior.addWidget(self.btn_enviar)
        self.layout.addLayout(self.layout_inferior)

        self.statusBar().showMessage("Estado: No registrado (Solo lectura)")

    def registrar_usuario(self):
        """Petición POST al endpoint /registro"""
        nombre, ok1 = QInputDialog.getText(self, "Registro", "Crea un nombre de usuario:")
        if ok1 and nombre:
            password, ok2 = QInputDialog.getText(self, "Registro", "Crea una contraseña:", QLineEdit.EchoMode.Password)
            if ok2 and password:
                try:
                    payload = {"user": nombre, "password": password}
                    response = requests.post(f"{self.url_base}/registro", json=payload)
                    
                    if response.status_code == 201:
                        self.usuario_actual = nombre
                        self.statusBar().showMessage(f"Online: {self.usuario_actual}")
                        QMessageBox.information(self, "Éxito", "Cuenta creada exitosamente.")
                    else:
                        error_msg = response.json().get('error', 'Error al registrar')
                        QMessageBox.warning(self, "Error de Registro", error_msg)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Servidor no disponible: {e}")

    def iniciar_sesion(self):
        """Petición POST al endpoint /login"""
        nombre, ok1 = QInputDialog.getText(self, "Inicio de Sesión", "Nombre de usuario:")
        if ok1 and nombre:
            password, ok2 = QInputDialog.getText(self, "Inicio de Sesión", "Contraseña:", QLineEdit.EchoMode.Password)
            if ok2 and password:
                try:
                    payload = {"user": nombre, "password": password}
                    response = requests.post(f"{self.url_base}/login", json=payload)
                    
                    if response.status_code == 200:
                        self.usuario_actual = nombre
                        self.statusBar().showMessage(f"Online: {self.usuario_actual}")
                        QMessageBox.information(self, "Éxito", f"Bienvenido {nombre}")
                    else:
                        # Aquí capturará el error si el usuario no existe (404) o clave errónea (401)
                        error_msg = response.json().get('error', 'Fallo de autenticación')
                        QMessageBox.warning(self, "Error de Acceso", error_msg)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error de conexión: {e}")

    def actualizar_chat(self):
        """Implementación de GET para obtener mensajes"""
        try:
            response = requests.get(f"{self.url_base}/mensajes")
            if response.status_code == 200:
                mensajes = response.json()
                self.caja_chat.clear()
                
                for msg in mensajes:
                    nombre = msg['usuario']
                    texto = msg['texto']
                    color = "blue" if nombre == self.usuario_actual else "darkgreen"
                    if nombre == "Sistema": color = "red"
                    
                    self.caja_chat.append(f"<b style='color:{color}'>{nombre}:</b> {texto}")
                
                self.caja_chat.moveCursor(QTextCursor.MoveOperation.End)
        except:
            pass 

    def enviar_mensaje(self):
        """Implementación de POST para enviar mensajes"""
        if not self.usuario_actual:
            QMessageBox.warning(self, "Error", "Debes iniciar sesión para escribir.")
            return

        texto = self.input_mensaje.text().strip()
        if texto:
            payload = {"user": self.usuario_actual, "text": texto}
            try:
                response = requests.post(f"{self.url_base}/mensajes", json=payload)
                if response.status_code == 201:
                    self.input_mensaje.clear()
                elif response.status_code == 403:
                    self.usuario_actual = None
                    self.statusBar().showMessage("Estado: Offline (Sesión expirada)")
                    QMessageBox.critical(self, "Error", "Sesión no iniciada. Por favor acceda con su cuenta.")
            except:
                QMessageBox.critical(self, "Error", "Error de conexión al enviar.")

    def closeEvent(self, event):
        """Logout automático al cerrar la app"""
        if self.usuario_actual:
            try:
                requests.post(f"{self.url_base}/logout", json={"user": self.usuario_actual}, timeout=1)
            except:
                pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())