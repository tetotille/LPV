# Lenguaje de Programación Visual

### Ingeniería Mecatrónica

**Semana 3: Python requests**


`requests` es una librería de Python que permite realizar peticiones HTTP. Antes o después, en algún proyecto, es posible que tengas que hacer peticiones web, ya sea para consumir un API, extraer información de una página o enviar el contenido de un formulario de manera automatizada

HTTP es un protocolo de transferencia de información que se utiliza para comunicar entre un servidor y un cliente. En el contexto de la programación, HTTP se utiliza para realizar peticiones a un servidor web y recibir respuestas de dicha petición

**Instalación de dependencias**

Agrega `requests` al proyecto usando poetry:

```bash
poetry add requests
```

Verifica la instalación:

```bash
poetry run python -c "import requests"
```


## Tabla de peticiones HTTP

En HTTP, las peticiones se realizan utilizando diferentes métodos, cada uno de ellos tiene un significado específico y se utilizan para realizar diferentes acciones en un recurso específico.

Petición | Descripción | Metodo en `requests`
--- | --- | ---
GET | Solicita información | requests.get() 
POST | Envía información | requests.post()
PUT | Actualiza información | requests.put()
PATCH | Actualiza información parcialmente | requests.patch()
DELETE | Elimina un recurso | requests.delete()
HEAD | Devuelve solo la cabecera | requests.head()
OPTIONS | Devuelve información sobre las opciones | requests.options()

## Ejemplos básicos

Para interactuar con una API, usualmente envíamos un JASON y recibimos un codigo de estado (Status Code), los mas comunes son los siguientes:

Codigo de estado | Descripción
--- | ---
200 - 299 | 200: `OK`, 201: `Created`, 204: `No Content`, etc.
300 - 399 | 300: `Multiple Choices`, 301: `Moved Permanently`, 304: `Not Modified`, etc.
400 - 499 | 400: `Bad Request`, 401: `Unauthorized`, 404: `Not Found`, etc.
500 - 599 | 500: `Internal Server Error`, 501: `Not Implemented`, etc.

### 1. Petición GET (Lectura)
Se utiliza para obtener datos del servidor sin modificar su estado.
```python
url = "http://127.0.0.1:5000/mensajes"
try:
    response = requests.get(url, timeout=5)
    # 200 OK: La petición fue exitosa
    if response.status_code == 200:
        print("Mensajes recibidos:", response.json())
    else:
        print(f"Error técnico {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Error: No se pudo conectar con el servidor.")
```

### 2. Petición POST (Escritura/Creación)
Se utiliza para enviar datos nuevos al servidor, como registrar un usuario o enviar un mensaje.
```python
url = "http://127.0.0.1:5000/registro"
data = {"user": "Carlos", "password": "123"}
response = requests.post(url, json=data)

# 201 Created: El recurso se creó con éxito
if response.status_code == 201:
    print("Registro exitoso:", response.json())
# 409 Conflict: El usuario ya existe
elif response.status_code == 409:
    print("Error: El usuario ya está registrado.")
```

### 3. Petición PUT
Se utiliza para actualizar un recurso existente reemplazándolo por completo. Si faltan campos en el envío, el servidor podría borrarlos en el recurso original.
```python
# Actualizar el mensaje con ID 1
url = "http://127.0.0.1:5000/mensajes/1"
data = {"user": "Carlos", "text": "Mensaje modificado por completo"}
response = requests.put(url, json=data)

if response.status_code == 200:
    print("Recurso reemplazado correctamente.")
```

### 4. Petición PATCH
Se utiliza una actualización parcial de datos
```python
url = "http://127.0.0.1:5000/usuarios/carlos"
data = {"password": "nueva_password_456"} # Solo enviamos el campo a cambiar
response = requests.patch(url, json=data)

if response.status_code == 200:
    print("Campo actualizado con éxito.")
``` 

### 5. Petición DELETE
Se utiliza para eliminar datos del servidor
```python
# Eliminar el mensaje con ID 5
url = "http://127.0.0.1:5000/mensajes/5"
response = requests.delete(url)

# 200 OK o 240 No Content son respuestas comunes para éxito
if response.status_code == 200:
    print("Mensaje eliminado permanentemente.")
elif response.status_code == 404:
    print("Error: El mensaje no existe.")
```

### 6. Petición HEAD
Es idéntica a GET, pero no descarga el cuerpo de la respuesta. Útil para verificar si un archivo existe o leer sus cabeceras.
```python
url = "http://127.0.0.1:5000/mensajes"
response = requests.head(url)
print(f"Tipo de contenido: {response.headers.get('Content-Type')}")
print(f"Código de respuesta: {response.status_code}")
```

### 7. Petición OPTIONS
Muestra información sobre las opciones de una petición
```python
url = "http://127.0.0.1:5000/mensajes"
response = requests.options(url)
print("Métodos permitidos:", response.headers.get('Allow'))
```

# Ejercicio

Desarrollar una interfaz gráfica (GUI) en `PyQt6` que funcione como cliente para un sistema de chat grupal, utilizando la librería `requests` para interactuar con un servidor API REST mediante el protocolo HTTP.

**Elementos de la interfaz:**

La aplicación debe incluir de forma obligatoria los siguientes componentes:

- Barra de menu:
    - Menu > Iniciar Sesión: Abre un diálogo para registrar o iniciar sesión
    - Menu > Registrarse: Abre un diálogo para registrar un nuevo usuario
    - Menu > Salir: Finaliza la sesion y cierra la aplicación

- Panel de visualización de Chat: Un area de texto (`QTextEdit`) de solo lectura donde se visualizarán los mensajes recibidos.

- Panel de Control Inferior: Con un `QLineEdit` para escribir el mensaje y un `QPushButton` para enviar el mensaje.

- Panel de Estado: Debe mostrar el estado de conexión del usuario actual (Online: Usuario o Offline: Sesión expirada).

**API REST**

El servidor implementa rutas específicas para garantizar que solo usuarios autenticados y con sesión activa puedan participar.

Accion | Método | Endpoint | Comportamiento esperado
--- | --- | --- | ---
Registro | POST | `/registro` | Crear un nuevo usuario. Si ya existe, devuelve un error 409.
Login | POST | `/login` | Verificar la autenticidad del usuario. Si existe no existe, devuelve un error 404.
Obtener Chat | GET | `/mensajes` | Retorna los mensajes recibidos en formato JSON.
Enviar mensaje | POST | `/mensajes` | Envia un mensaje al servidor.
Logout | POST | `/logout` | Cierra la sesión del usuario.

**Requisitos de logica:**
1. Implementar un `QTimer` para actualizar los mensajes cada 2 segundos.
2. Al cerrar la ventana, realizar un logout automático
3. Si el servidor responde con un error, el cliente debe limpiar el estado del usuario y solicitar una nueva sesión.
4. El campo de contraseña debe ocultar los caracteres.

Para probar su aplicacion
1. Lanzar el servidor con:
```bash
python server.py
```
2. Lanzar la aplicación con:
```bash
python app.py
```

El servidor corre por defecto en `http://127.0.0.1:5000`

