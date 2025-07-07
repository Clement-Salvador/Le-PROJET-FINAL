from flask import Flask, jsonify
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    """
    Renvoie un message de Bienvenue
    """
    return "Bienvenue sur la Gateway Flask !"

@app.route('/health', methods=['GET'])
def get_health():
    """
    Renvoie le status de l'API
    ---
    responses:
      200:
        description: status OK
      500:
        description: status KO
    """
    try:
        return jsonify({'status': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'KO', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)