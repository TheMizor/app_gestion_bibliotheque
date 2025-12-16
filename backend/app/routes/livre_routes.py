"""
Routes pour la gestion des livres
"""
from flask import Blueprint, request, jsonify
from app.services.livre_service import LivreService
from app.utils.auth import require_auth, require_role
from app.models.utilisateur import Role

livre_bp = Blueprint('livres', __name__, url_prefix='/api/books')


@livre_bp.route('', methods=['GET'])
@require_auth
def get_livres(utilisateur):
    """Récupérer la liste des livres avec pagination et filtres"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    search = request.args.get('search', None)
    available = request.args.get('available', 'false').lower() == 'true'
    
    livre_service = LivreService()
    result = livre_service.get_all(
        page=page,
        limit=limit,
        search=search,
        available_only=available
    )
    
    return jsonify({
        'books': [livre.to_dict() for livre in result['livres']],
        'total': result['total'],
        'page': result['page'],
        'limit': result['limit']
    }), 200


@livre_bp.route('/<int:livre_id>', methods=['GET'])
@require_auth
def get_livre(utilisateur, livre_id):
    """Récupérer un livre par son ID"""
    livre_service = LivreService()
    livre = livre_service.get_by_id(livre_id)
    
    if not livre:
        return jsonify({'error': 'Livre non trouvé'}), 404
    
    return jsonify(livre.to_dict()), 200


@livre_bp.route('', methods=['POST'])
@require_role(Role.BIBLIOTHECAIRE)
def create_livre(utilisateur):
    """Créer un nouveau livre (Bibliothécaire uniquement)"""
    data = request.get_json()
    
    if not data or not data.get('titre') or not data.get('auteur'):
        return jsonify({'error': 'Titre et auteur requis'}), 400
    
    livre_service = LivreService()
    livre = livre_service.create(
        titre=data['titre'],
        auteur=data['auteur'],
        isbn=data.get('isbn'),
        nombre_exemplaires=data.get('nombre_exemplaires', 1)
    )
    
    return jsonify(livre.to_dict()), 201


@livre_bp.route('/<int:livre_id>', methods=['PUT'])
@require_role(Role.BIBLIOTHECAIRE)
def update_livre(utilisateur, livre_id):
    """Mettre à jour un livre (Bibliothécaire uniquement)"""
    data = request.get_json()
    
    livre_service = LivreService()
    livre = livre_service.update(
        livre_id=livre_id,
        titre=data.get('titre'),
        auteur=data.get('auteur'),
        isbn=data.get('isbn'),
        nombre_exemplaires=data.get('nombre_exemplaires')
    )
    
    if not livre:
        return jsonify({'error': 'Livre non trouvé'}), 404
    
    return jsonify(livre.to_dict()), 200


@livre_bp.route('/<int:livre_id>', methods=['DELETE'])
@require_role(Role.BIBLIOTHECAIRE)
def delete_livre(utilisateur, livre_id):
    """Supprimer un livre (Bibliothécaire uniquement)"""
    livre_service = LivreService()
    deleted = livre_service.delete(livre_id)
    
    if not deleted:
        return jsonify({'error': 'Livre non trouvé'}), 404
    
    return jsonify({'message': 'Livre supprimé avec succès'}), 200

