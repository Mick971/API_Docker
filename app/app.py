from flask import Flask, jsonify, request, render_template, render_template_string

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

@app.route('/formulario', methods=['GET'])
def mostrar_formulario():
    return render_template('formulario.html')

@app.route('/evaluar-password', methods=['POST'])
def evaluar_password():
    # Detectar si los datos vienen en formato JSON o formulario
    if request.is_json:
        data = request.get_json()
        password = data.get('password', '')
    else:
        password = request.form.get('password', '')

    if not password:
        return "Debes proporcionar una contraseña para evaluar.", 400

    # Evaluar la contraseña
    puntuacion = 0
    recomendaciones = []

    if len(password) >= 12:
        puntuacion += 2
    elif len(password) >= 8:
        puntuacion += 1
    else:
        recomendaciones.append("Usa al menos 8 caracteres")

    if any(c.islower() for c in password):
        puntuacion += 1
    else:
        recomendaciones.append("Incluye letras minúsculas")

    if any(c.isupper() for c in password):
        puntuacion += 1
    else:
        recomendaciones.append("Incluye letras mayúsculas")

    if any(c.isdigit() for c in password):
        puntuacion += 1
    else:
        recomendaciones.append("Agrega números")

    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/~" for c in password):
        puntuacion += 1
    else:
        recomendaciones.append("Usa caracteres especiales")

    nivel = "Débil"
    color = "red"
    if puntuacion >= 5:
        nivel = "Muy fuerte"
        color = "green"
    elif puntuacion >= 3:
        nivel = "Intermedia"
        color = "orange"

    html_template = f"""
    <html>
    <head>
        <title>Evaluación de Contraseña</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                padding: 40px;
                color: #333;
            }}
            .resultado {{
                background-color: #fff;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
                max-width: 600px;
                margin: auto;
            }}
            .nivel {{
                font-size: 22px;
                font-weight: bold;
                color: {color};
            }}
            ul {{
                padding-left: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="resultado">
            <h2>Evaluación de tu Contraseña</h2>
            <p><strong>Contraseña:</strong> {"*" * len(password)}</p>
            <p><strong>Puntuación:</strong> {puntuacion} / 6</p>
            <p class="nivel">Nivel de seguridad: {nivel}</p>
            {"<p>¡Buena contraseña! ✅</p>" if not recomendaciones else "<p>Recomendaciones para mejorar:</p><ul>" + "".join(f"<li>{r}</li>" for r in recomendaciones) + "</ul>"}
        </div>
    </body>
    </html>
    """

    return render_template_string(html_template)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


