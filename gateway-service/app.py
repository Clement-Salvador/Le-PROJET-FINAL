from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def get_health():
    try:
        return jsonify({'status': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'KO', 'error': str(e)}), 500
