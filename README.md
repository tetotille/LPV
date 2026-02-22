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
200, 201 | Petición correcta
404 | Recurso no encontrado
500 | Error interno del servidor

### 1. Petición GET
Se utiliza para obtener datos del servidor.
```python
url_api = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url_api)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

### 2. Petición POST
Se utiliza para enviar datos al servidor.
```python
url_api = "https://jsonplaceholder.typicode.com/posts"
data = {"user": "Carlos", "text": "Esto es un mensaje"}
response = requests.post(url_api, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

### 3. Petición PUT
Se utiliza para actualizar por completo los datos en el servidor
```python
url_api = "https://jsonplaceholder.typicode.com/posts/1"
data = {"user": "Carlos", "text": "Esto es un mensaje nuevo"}
response = requests.put(url_api, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

### 4. Petición PATCH
Se utiliza para actualizar solo algunos datos del servidor
```python
url_api = "https://jsonplaceholder.typicode.com/posts/1"
data = {"user": "Carlos"}
response = requests.patch(url_api, json=data)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
``` 

### 5. Petición DELETE
Se utiliza para eliminar datos del servidor
```python
url_api = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.delete(url_api)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")

### 6. Petición HEAD
Similar a GET, pero solo devuelve la cabecera del recurso
```python
url_api = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.head(url_api)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

### 7. Petición OPTIONS
Muestra información sobre las opciones de una petición
```python
url_api = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.options(url_api)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

# Ejercicio

Desarrolle un interfaz grafica que emplee la librería `requests` para realizar peticiones HTTP como cliente de un chat grupal. 

En el chat, los usuarios podrán enviar, recibir y eliminar mensajes de texto.

La interfaz debe ser desarrollada en PyQt6 y debe incluir los siguientes elementos graficos:

- Una barra de menú con las obciones Menu > Iniciar Chat, Registrarse y Salir
- Una panel principal donde se visualizará el chat, los chats de cada usuario seran de un color distintivo
- Un panel de control en la parte inferior con un botón de enviar mensaje y un campo de texto para escribir el mensaje

Para gestionar los mensajes:
- Mostrar los mensajes del chat en un listado: GET
- Registrar un usuario, enviar un mensaje: POST
- Editar un mensaje: PUT
- Eliminar un mensaje: DELETE

OBS: Recuerde usar `QTimer` para actualizar la lista de mensajes cada 2 segundos.

Para lanzar el servidor descargue y ejecute el archivo `server.py` en una terminal aparte.
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos en memoria
usuarios_db = {}        # {usuario: password}
usuarios_online = set() # Usuarios con sesión activa
mensajes = [{"id": 1, "usuario": "Sistema", "texto": "Servidor listo. Use el menú para Registrarse o Iniciar Sesión."}]
contador_id = 2

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.json
    usuario = data.get('user')
    password = data.get('password')
    
    if not usuario or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    if usuario in usuarios_db:
        return jsonify({"error": "El usuario ya existe"}), 409

    usuarios_db[usuario] = password
    usuarios_online.add(usuario) # Login automático tras registro
    print(f"Nuevo registro: {usuario}")
    return jsonify({"status": "Usuario creado y conectado"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('user')
    password = data.get('password')
    
    if not usuario or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    # VALIDACIÓN CLAVE: Si no existe, error (no se registra automáticamente)
    if usuario not in usuarios_db:
        return jsonify({"error": "El usuario no está registrado"}), 404
    
    if usuarios_db[usuario] == password:
        usuarios_online.add(usuario)
        print(f"Login exitoso: {usuario}")
        return jsonify({"status": "Sesión iniciada"}), 200
    else:
        return jsonify({"error": "Contraseña incorrecta"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    usuario = request.json.get('user')
    if usuario in usuarios_online:
        usuarios_online.remove(usuario)
    return jsonify({"status": "Offline"}), 200

@app.route('/mensajes', methods=['GET'])
def obtener_mensajes():
    return jsonify(mensajes), 200

@app.route('/mensajes', methods=['POST'])
def enviar_mensaje():
    global contador_id
    data = request.json
    usuario = data.get('user')
    texto = data.get('text')

    if usuario not in usuarios_online:
        return jsonify({"error": "Sesión no iniciada"}), 403

    nuevo_mensaje = {"id": contador_id, "usuario": usuario, "texto": texto}
    mensajes.append(nuevo_mensaje)
    contador_id += 1
    return jsonify(nuevo_mensaje), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```





