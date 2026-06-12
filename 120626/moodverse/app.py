from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Diccionario con la información y frases para cada estado de ánimo
MOOD_DATA = {
    "electrico": {
        "frase": "⚡ El futuro pertenece a quienes creen en la belleza de sus sueños más intensos. ¡Rompe los límites hoy!",
        "autor": "Energía Pura"
    },
    "zen": {
        "frase": "🍃 Respira. El caos es solo el fondo sobre el cual pintas tu paz interior. Todo fluye a su propio ritmo.",
        "autor": "Calma Profunda"
    },
    "melancolico": {
        "frase": "🌌 En la inmensidad del espacio, cada lágrima es una estrella titilando en la oscuridad de tu propia galaxia.",
        "autor": "Cosmos Interior"
    },
    "creativo": {
        "frase": "💥 La creatividad es la inteligencia divirtiéndose. Deja que el caos de tu mente cree arte inesperado.",
        "autor": "Mente Explosiva"
    }
}

@app.route('/')
def home():
    # Renderiza la página principal
    return render_template('index.html')

@app.route('/api/mood/<tipo>')
def get_mood_data(tipo):
    # Endpoint que devuelve la frase según el mood seleccionado
    data = MOOD_DATA.get(tipo, {"frase": "Explora tu universo interno.", "autor": "MoodVerse"})
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)