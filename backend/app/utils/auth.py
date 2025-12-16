"""
Utilitaires pour l'authentification JWT
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config import Config
from app.services.utilisateur_service import UtilisateurService


def generate_token(utilisateur_id, role):
    """Générer un token JWT pour un utilisateur"""
    payload = {
        'user_id': utilisateur_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=Config().JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, Config().JWT_SECRET_KEY, algorithm=Config().JWT_ALGORITHM)
    return token


def verify_token(token):
    """Vérifier et décoder un token JWT"""
    try:
        payload = jwt.decode(token, Config().JWT_SECRET_KEY, algorithms=[Config().JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user():
    """Récupérer l'utilisateur actuel depuis le token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(' ')[1]  # Format: "Bearer <token>"
        payload = verify_token(token)
        
        if not payload:
            return None
        
        utilisateur_service = UtilisateurService()
        utilisateur = utilisateur_service.get_by_id(payload['user_id'])
        return utilisateur
    except (IndexError, KeyError):
        return None


def require_auth(f):
    """Décorateur pour protéger une route avec authentification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        utilisateur = get_current_user()
        if not utilisateur:
            return jsonify({'error': 'Authentification requise'}), 401
        return f(utilisateur, *args, **kwargs)
    return decorated_function


def require_role(*allowed_roles):
    """Décorateur pour protéger une route avec vérification de rôle"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            utilisateur = get_current_user()
            if not utilisateur:
                return jsonify({'error': 'Authentification requise'}), 401
            if utilisateur.role not in allowed_roles:
                return jsonify({'error': 'Accès interdit'}), 403
            return f(utilisateur, *args, **kwargs)
        return decorated_function
    return decorator

