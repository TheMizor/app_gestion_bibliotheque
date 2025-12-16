"""
Routes pour la gestion des emprunts
"""
from flask import Blueprint, request, jsonify
from app.services.emprunt_service import EmpruntService
from app.services.livre_service import LivreService
from app.utils.auth import require_auth, require_role
from app.models.utilisateur import Role

emprunt_bp = Blueprint('emprunts', __name__, url_prefix='/api/loans')


@emprunt_bp.route('', methods=['GET'])
@require_auth
def get_emprunts(utilisateur):
    """Récupérer la liste des emprunts"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    statut = request.args.get('status', None)
    livre_id = request.args.get('book_id', None, type=int)
    
    # Un utilisateur ne peut voir que ses propres emprunts (sauf bibliothécaire)
    user_id_filter = None if utilisateur.is_bibliothecaire() else utilisateur.id
    
    emprunt_service = EmpruntService()
    result = emprunt_service.get_all(
        page=page,
        limit=limit,
        utilisateur_id=user_id_filter,
        statut=statut,
        livre_id=livre_id
    )
    
    emprunts_data = []
    for emprunt in result['emprunts']:
        emprunt_dict = emprunt.to_dict()
        # Ajouter les informations supplémentaires
        if hasattr(emprunt, 'livre_titre'):
            emprunt_dict['book_title'] = emprunt.livre_titre
            emprunt_dict['book_author'] = emprunt.livre_auteur
        if hasattr(emprunt, 'utilisateur_nom'):
            emprunt_dict['user_name'] = emprunt.utilisateur_nom
            emprunt_dict['user_email'] = emprunt.utilisateur_email
        emprunts_data.append(emprunt_dict)
    
    return jsonify({
        'loans': emprunts_data,
        'total': result['total'],
        'page': result['page'],
        'limit': result['limit']
    }), 200


@emprunt_bp.route('/<int:emprunt_id>', methods=['GET'])
@require_auth
def get_emprunt(utilisateur, emprunt_id):
    """Récupérer un emprunt par son ID"""
    emprunt_service = EmpruntService()
    emprunt = emprunt_service.get_by_id(emprunt_id)
    
    if not emprunt:
        return jsonify({'error': 'Emprunt non trouvé'}), 404
    
    # Un utilisateur ne peut voir que ses propres emprunts (sauf bibliothécaire)
    if not utilisateur.is_bibliothecaire() and emprunt.utilisateur_id != utilisateur.id:
        return jsonify({'error': 'Accès interdit'}), 403
    
    emprunt_dict = emprunt.to_dict()
    if hasattr(emprunt, 'livre_titre'):
        emprunt_dict['book_title'] = emprunt.livre_titre
        emprunt_dict['book_author'] = emprunt.livre_auteur
    if hasattr(emprunt, 'utilisateur_nom'):
        emprunt_dict['user_name'] = emprunt.utilisateur_nom
        emprunt_dict['user_email'] = emprunt.utilisateur_email
    
    return jsonify(emprunt_dict), 200


@emprunt_bp.route('', methods=['POST'])
@require_auth
def create_emprunt(utilisateur):
    """Créer un nouvel emprunt"""
    data = request.get_json()
    
    if not data or not data.get('book_id'):
        return jsonify({'error': 'ID du livre requis'}), 400
    
    livre_id = data['book_id']
    user_id = data.get('user_id', utilisateur.id)
    
    # Seuls les bibliothécaires peuvent créer des emprunts pour d'autres utilisateurs
    if user_id != utilisateur.id and not utilisateur.is_bibliothecaire():
        return jsonify({'error': 'Accès interdit'}), 403
    
    # Vérifier que le livre est disponible
    livre_service = LivreService()
    livre = livre_service.get_by_id(livre_id)
    
    if not livre:
        return jsonify({'error': 'Livre non trouvé'}), 404
    
    if livre.exemplaires_disponibles <= 0:
        return jsonify({'error': 'Livre non disponible'}), 400
    
    # Créer l'emprunt
    emprunt_service = EmpruntService()
    duree_jours = data.get('duree_jours', 30)
    emprunt = emprunt_service.create(livre_id, user_id, duree_jours)
    
    # Décrémenter les exemplaires disponibles
    livre_service.decrementer_exemplaires_disponibles(livre_id)
    
    emprunt_dict = emprunt.to_dict()
    if hasattr(emprunt, 'livre_titre'):
        emprunt_dict['book_title'] = emprunt.livre_titre
        emprunt_dict['book_author'] = emprunt.livre_auteur
    if hasattr(emprunt, 'utilisateur_nom'):
        emprunt_dict['user_name'] = emprunt.utilisateur_nom
        emprunt_dict['user_email'] = emprunt.utilisateur_email
    
    return jsonify(emprunt_dict), 201


@emprunt_bp.route('/<int:emprunt_id>/return', methods=['PUT'])
@require_auth
def retourner_livre(utilisateur, emprunt_id):
    """Retourner un livre emprunté"""
    emprunt_service = EmpruntService()
    emprunt = emprunt_service.get_by_id(emprunt_id)
    
    if not emprunt:
        return jsonify({'error': 'Emprunt non trouvé'}), 404
    
    # Un utilisateur ne peut retourner que ses propres emprunts (sauf bibliothécaire)
    if not utilisateur.is_bibliothecaire() and emprunt.utilisateur_id != utilisateur.id:
        return jsonify({'error': 'Accès interdit'}), 403
    
    if emprunt.statut == 'retourne':
        return jsonify({'error': 'Livre déjà retourné'}), 400
    
    # Retourner le livre
    emprunt_retourne = emprunt_service.retourner(emprunt_id)
    
    if not emprunt_retourne:
        return jsonify({'error': 'Erreur lors du retour'}), 400
    
    # Incrémenter les exemplaires disponibles
    livre_service = LivreService()
    livre_service.incrementer_exemplaires_disponibles(emprunt.livre_id)
    
    emprunt_dict = emprunt_retourne.to_dict()
    if hasattr(emprunt_retourne, 'livre_titre'):
        emprunt_dict['book_title'] = emprunt_retourne.livre_titre
        emprunt_dict['book_author'] = emprunt_retourne.livre_auteur
    if hasattr(emprunt_retourne, 'utilisateur_nom'):
        emprunt_dict['user_name'] = emprunt_retourne.utilisateur_nom
        emprunt_dict['user_email'] = emprunt_retourne.utilisateur_email
    
    return jsonify(emprunt_dict), 200

