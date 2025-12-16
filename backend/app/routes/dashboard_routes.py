"""
Routes pour le tableau de bord (Bibliothécaires uniquement)
"""
from flask import Blueprint, jsonify
from app.services.emprunt_service import EmpruntService
from app.services.livre_service import LivreService
from app.services.utilisateur_service import UtilisateurService
from app.utils.auth import require_role
from app.models.utilisateur import Role

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/stats', methods=['GET'])
@require_role(Role.BIBLIOTHECAIRE)
def get_stats(utilisateur):
    """Récupérer les statistiques générales (Bibliothécaire uniquement)"""
    livre_service = LivreService()
    utilisateur_service = UtilisateurService()
    emprunt_service = EmpruntService()
    
    # Statistiques des livres
    livres_result = livre_service.get_all(page=1, limit=1)
    total_livres = livres_result['total']
    
    # Statistiques des utilisateurs
    users_result = utilisateur_service.get_all(page=1, limit=1)
    total_users = users_result['total']
    
    # Statistiques des emprunts
    emprunts_actifs = emprunt_service.get_all(statut='actif', page=1, limit=1)
    emprunts_retard = emprunt_service.get_emprunts_en_retard()
    
    total_emprunts_actifs = emprunts_actifs['total']
    total_emprunts_retard = len(emprunts_retard)
    
    # Calculer le taux de retard
    taux_retard = 0
    if total_emprunts_actifs > 0:
        taux_retard = (total_emprunts_retard / total_emprunts_actifs) * 100
    
    # Livres les plus populaires (requête SQL directe nécessaire pour cette fonctionnalité)
    # Pour l'instant, on retourne une structure vide
    popular_books = []
    
    return jsonify({
        'total_books': total_livres,
        'total_users': total_users,
        'active_loans': total_emprunts_actifs,
        'overdue_loans': total_emprunts_retard,
        'overdue_rate': round(taux_retard, 2),
        'popular_books': popular_books
    }), 200


@dashboard_bp.route('/notifications', methods=['GET'])
@require_role(Role.BIBLIOTHECAIRE)
def get_notifications(utilisateur):
    """Récupérer les notifications de rappels (Bibliothécaire uniquement)"""
    emprunt_service = EmpruntService()
    
    # Mettre à jour les statuts en retard
    emprunt_service.update_statut_retard()
    
    # Récupérer les rappels
    rappels_30 = emprunt_service.get_rappels_30_jours()
    rappels_5 = emprunt_service.get_rappels_5_jours()
    
    notifications = []
    
    for emprunt in rappels_30:
        notifications.append({
            'loan_id': emprunt.id,
            'user_name': emprunt.utilisateur_nom if hasattr(emprunt, 'utilisateur_nom') else None,
            'user_email': emprunt.utilisateur_email if hasattr(emprunt, 'utilisateur_email') else None,
            'book_title': emprunt.livre_titre if hasattr(emprunt, 'livre_titre') else None,
            'due_date': emprunt.date_retour_prevue.isoformat() if hasattr(emprunt.date_retour_prevue, 'isoformat') else str(emprunt.date_retour_prevue),
            'days_remaining': 30,
            'type': 'reminder_30'
        })
    
    for emprunt in rappels_5:
        notifications.append({
            'loan_id': emprunt.id,
            'user_name': emprunt.utilisateur_nom if hasattr(emprunt, 'utilisateur_nom') else None,
            'user_email': emprunt.utilisateur_email if hasattr(emprunt, 'utilisateur_email') else None,
            'book_title': emprunt.livre_titre if hasattr(emprunt, 'livre_titre') else None,
            'due_date': emprunt.date_retour_prevue.isoformat() if hasattr(emprunt.date_retour_prevue, 'isoformat') else str(emprunt.date_retour_prevue),
            'days_remaining': 5,
            'type': 'reminder_5'
        })
    
    return jsonify({
        'notifications': notifications,
        'total': len(notifications)
    }), 200

