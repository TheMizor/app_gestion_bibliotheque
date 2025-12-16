"""
Point d'entrée principal de l'application backend
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app.routes import auth_bp, livre_bp, utilisateur_bp, emprunt_bp, dashboard_bp

app = Flask(__name__)
app.config.from_object(Config)

# Activer CORS pour permettre les requêtes depuis le frontend
CORS(app)

# Enregistrer les blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(livre_bp)
app.register_blueprint(utilisateur_bp)
app.register_blueprint(emprunt_bp)
app.register_blueprint(dashboard_bp)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'API"""
    return jsonify({'status': 'ok', 'message': 'API fonctionnelle'}), 200


@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return jsonify({'error': 'Route non trouvée'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    return jsonify({'error': 'Erreur interne du serveur'}), 500


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
