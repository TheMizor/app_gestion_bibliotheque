"""
Routes pour la gestion des utilisateurs
"""
from flask import Blueprint, request, jsonify
from app.services.utilisateur_service import UtilisateurService
from app.utils.auth import require_auth, require_role
from app.models.utilisateur import Role

utilisateur_bp = Blueprint('utilisateurs', __name__, url_prefix='/api/users')


@utilisateur_bp.route('', methods=['GET'])
@require_role(Role.BIBLIOTHECAIRE)
def get_utilisateurs(utilisateur):
    """Récupérer la liste des utilisateurs (Bibliothécaire uniquement)"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    role_filter = request.args.get('role', None)
    
    utilisateur_service = UtilisateurService()
    result = utilisateur_service.get_all(
        page=page,
        limit=limit,
        role=role_filter
    )
    
    return jsonify({
        'users': [u.to_dict() for u in result['utilisateurs']],
        'total': result['total'],
        'page': result['page'],
        'limit': result['limit']
    }), 200


@utilisateur_bp.route('/<int:user_id>', methods=['GET'])
@require_auth
def get_utilisateur(utilisateur, user_id):
    """Récupérer un utilisateur par son ID"""
    # Un utilisateur peut voir son propre profil, un bibliothécaire peut voir tous les profils
    if utilisateur.id != user_id and not utilisateur.is_bibliothecaire():
        return jsonify({'error': 'Accès interdit'}), 403
    
    utilisateur_service = UtilisateurService()
    user = utilisateur_service.get_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify(user.to_dict()), 200


@utilisateur_bp.route('', methods=['POST'])
@require_role(Role.BIBLIOTHECAIRE)
def create_utilisateur(utilisateur):
    """Créer un nouvel utilisateur (Bibliothécaire uniquement)"""
    data = request.get_json()
    
    if not data or not data.get('nom') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Nom, email et mot de passe requis'}), 400
    
    role = data.get('role', Role.ETUDIANT)
    
    utilisateur_service = UtilisateurService()
    new_user = utilisateur_service.create(
        nom=data['nom'],
        email=data['email'],
        mot_de_passe=data['password'],
        role=role
    )
    
    if not new_user:
        return jsonify({'error': 'Cet email est déjà utilisé'}), 400
    
    return jsonify(new_user.to_dict()), 201


@utilisateur_bp.route('/<int:user_id>', methods=['PUT'])
@require_auth
def update_utilisateur(utilisateur, user_id):
    """Mettre à jour un utilisateur"""
    # Un utilisateur peut modifier son propre profil, un bibliothécaire peut modifier tous les profils
    if utilisateur.id != user_id and not utilisateur.is_bibliothecaire():
        return jsonify({'error': 'Accès interdit'}), 403
    
    data = request.get_json()
    
    # Seuls les bibliothécaires peuvent changer le rôle
    if 'role' in data and not utilisateur.is_bibliothecaire():
        return jsonify({'error': 'Seuls les bibliothécaires peuvent modifier les rôles'}), 403
    
    utilisateur_service = UtilisateurService()
    updated_user = utilisateur_service.update(
        utilisateur_id=user_id,
        nom=data.get('nom'),
        email=data.get('email'),
        mot_de_passe=data.get('password'),
        role=data.get('role') if utilisateur.is_bibliothecaire() else None
    )
    
    if not updated_user:
        return jsonify({'error': 'Utilisateur non trouvé ou email déjà utilisé'}), 404
    
    return jsonify(updated_user.to_dict()), 200


@utilisateur_bp.route('/<int:user_id>', methods=['DELETE'])
@require_role(Role.BIBLIOTHECAIRE)
def delete_utilisateur(utilisateur, user_id):
    """Supprimer un utilisateur (Bibliothécaire uniquement)"""
    utilisateur_service = UtilisateurService()
    deleted = utilisateur_service.delete(user_id)
    
    if not deleted:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200

