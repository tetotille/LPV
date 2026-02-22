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