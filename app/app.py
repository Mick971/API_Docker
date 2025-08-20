from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "API funcionando correctamente"})

@app.route('/saludo', methods=['GET'])
def saludo():
    nombre = request.args.get('nombre', 'invitado')
    return jsonify({"saludo": f"Hola, {nombre}!"})

@app.route('/seguridad', methods=['GET'])
def seguridad():
    tips = [
        "Usa contraseñas seguras",
        "No compartas tus credenciales",
        "Actualiza tu software regularmente",
        "Usa autenticación multifactor"
    ]
    return jsonify({"tips": tips})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


