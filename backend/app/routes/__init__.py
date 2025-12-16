# Routes API
from .auth_routes import auth_bp
from .livre_routes import livre_bp
from .utilisateur_routes import utilisateur_bp
from .emprunt_routes import emprunt_bp
from .dashboard_routes import dashboard_bp
from .notification_routes import notification_bp

__all__ = ['auth_bp', 'livre_bp', 'utilisateur_bp', 'emprunt_bp', 'dashboard_bp', 'notification_bp']
