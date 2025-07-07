from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur la Gateway Flask !"

@app.route('/health', methods=['GET'])
def get_health():
    try:
        return jsonify({'status': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'KO', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)