"""
Point d'entrée principal de l'application backend
"""
from flask import Flask
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Activer CORS pour permettre les requêtes depuis le frontend
CORS(app)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'API"""
    return {'status': 'ok', 'message': 'API fonctionnelle'}, 200


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
