from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulando una base de datos de usuarios
usuarios = {
    "usuario1": "password1",
    "usuario2": "password2"
}

# Valor fijo que se puede consultar y actualizar
valor_fijo = {"valor": 43}

# Token de autenticación (en un entorno real, se generaría un token dinámico)
TOKEN_VALIDO = "abc123"

@app.route('/')
def home():
    return "¡Te amo mi amorchis!"

# Endpoint de Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    password = data.get('password')
    
    if usuario in usuarios and usuarios[usuario] == password:
        return jsonify({"mensaje": "Login exitoso", "token": TOKEN_VALIDO, "status": "success"}), 200
    else:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos", "status": "failed"}), 401

# Endpoint GET Protegido
@app.route('/valor', methods=['GET'])
def obtener_valor():
    auth = request.headers.get('Authorization')
    
    if auth == f"Bearer {TOKEN_VALIDO}":
        return jsonify(valor_fijo), 200
    else:
        return jsonify({"mensaje": "No autorizado"}), 403

# Endpoint POST Protegido
@app.route('/valor', methods=['POST'])
def actualizar_valor():
    auth = request.headers.get('Authorization')
    
    if auth == f"Bearer {TOKEN_VALIDO}":
        data = request.json
        valor_fijo["valor"] = data.get('valor', valor_fijo["valor"])
        return jsonify({"mensaje": "Valor actualizado con éxito", "nuevo_valor": valor_fijo["valor"]}), 200
    else:
        return jsonify({"mensaje": "No autorizado"}), 403


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
