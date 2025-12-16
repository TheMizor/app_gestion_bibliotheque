"""
Routes d'authentification
"""
from flask import Blueprint, request, jsonify
from app.services.utilisateur_service import UtilisateurService
from app.utils.auth import generate_token, get_current_user, require_auth
from app.models.utilisateur import Role

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """Connexion d'un utilisateur"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email et mot de passe requis'}), 400
    
    utilisateur_service = UtilisateurService()
    utilisateur = utilisateur_service.get_by_email(data['email'])
    
    if not utilisateur:
        return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
    
    if not utilisateur_service.verify_password(utilisateur, data['password']):
        return jsonify({'error': 'Email ou mot de passe incorrect'}), 401
    
    token = generate_token(utilisateur.id, utilisateur.role)
    
    return jsonify({
        'token': token,
        'user': utilisateur.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user_info(utilisateur):
    """Récupérer les informations de l'utilisateur connecté"""
    return jsonify(utilisateur.to_dict()), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur (réservé aux bibliothécaires ou public selon besoin)"""
    data = request.get_json()
    
    if not data or not data.get('nom') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Nom, email et mot de passe requis'}), 400
    
    role = data.get('role', Role.ETUDIANT)
    
    # Vérifier que seul un bibliothécaire peut créer d'autres bibliothécaires
    if role == Role.BIBLIOTHECAIRE:
        current_user = get_current_user()
        if not current_user or not current_user.is_bibliothecaire():
            return jsonify({'error': 'Seuls les bibliothécaires peuvent créer des comptes bibliothécaires'}), 403
    
    utilisateur_service = UtilisateurService()
    utilisateur = utilisateur_service.create(
        nom=data['nom'],
        email=data['email'],
        mot_de_passe=data['password'],
        role=role
    )
    
    if not utilisateur:
        return jsonify({'error': 'Cet email est déjà utilisé'}), 400
    
    token = generate_token(utilisateur.id, utilisateur.role)
    
    return jsonify({
        'token': token,
        'user': utilisateur.to_dict()
    }), 201

