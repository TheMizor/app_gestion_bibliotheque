"""
Point d'entrée principal de l'application backend
"""
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app.routes import auth_bp, livre_bp, utilisateur_bp, emprunt_bp, dashboard_bp, notification_bp
from app.scheduler import NotificationScheduler

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
app.register_blueprint(notification_bp)

# Initialiser le scheduler de notifications
scheduler = NotificationScheduler()


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
    try:
        # Démarrer le scheduler si on n'est pas en mode test
        if not app.config.get('TESTING', False):
            scheduler.demarrer()
        
        app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.arreter()
