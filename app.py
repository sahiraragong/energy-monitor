from flask import Flask, request, render_template_string

app = Flask(__name__)

# Almacenamiento temporal en memoria
latest_data = {
    'voltage': 0.0,
    'current': 0.0,
    'power': 0.0,
    'energy': 0.0,
    'frequency': 0.0,
    'pf': 0.0
}

@app.route('/api/measurements', methods=['POST'])
def receive_data():
    global latest_data
    if not request.is_json:
        return {"status": "error", "message": "Content-Type must be application/json"}, 400

    data = request.get_json()
    required_fields = latest_data.keys()

    if not all(field in data for field in required_fields):
        return {"status": "error", "message": "Faltan campos requeridos"}, 400

    latest_data = {key: float(data[key]) for key in required_fields}
    return {"status": "success", "message": "Datos actualizados"}, 200

@app.route('/')
def dashboard():
    cards = ""
    colors = {
        'voltage': 'blue',
        'current': 'green',
        'power': 'red',
        'energy': 'yellow',
        'frequency': 'purple',
        'pf': 'indigo'
    }

    for key, value in latest_data.items():
        unit = {
            'voltage': 'V',
            'current': 'A',
            'power': 'W',
            'energy': 'kWh',
            'frequency': 'Hz',
            'pf': ''
        }[key]

        cards += f"""
        <div class="p-4 bg-{colors[key]}-100 text-{colors[key]}-800 rounded-lg shadow-md">
            <p class="text-sm font-medium opacity-80">{key.capitalize()}</p>
            <p class="text-4xl font-extrabold mt-1">{value:.2f} <span class="text-xl font-semibold ml-1 opacity-70">{unit}</span></p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Monitor de Energía</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 p-6">
        <h1 class="text-3xl font-bold text-center mb-6">Monitor de Energía PZEM-004T</h1>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {cards}
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
