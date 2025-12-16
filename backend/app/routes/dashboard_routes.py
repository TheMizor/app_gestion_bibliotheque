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
    
    # Compter les livres disponibles
    livres_disponibles_result = livre_service.get_all(page=1, limit=1, available_only=True)
    total_livres_disponibles = livres_disponibles_result['total']
    
    # Statistiques des utilisateurs
    users_result = utilisateur_service.get_all(page=1, limit=1)
    total_users = users_result['total']
    
    # Statistiques par rôle
    stats_par_role = utilisateur_service.get_all(page=1, limit=1000)
    users_par_role = {}
    for user in stats_par_role['utilisateurs']:
        role = user.role
        if role not in users_par_role:
            users_par_role[role] = 0
        users_par_role[role] += 1
    
    # Statistiques des emprunts
    emprunts_actifs = emprunt_service.get_all(statut='actif', page=1, limit=1)
    emprunts_retard = emprunt_service.get_emprunts_en_retard()
    emprunts_retournes = emprunt_service.get_all(statut='retourne', page=1, limit=1)
    
    total_emprunts_actifs = emprunts_actifs['total']
    total_emprunts_retard = len(emprunts_retard)
    total_emprunts_retournes = emprunts_retournes['total']
    total_emprunts_total = total_emprunts_actifs + total_emprunts_retournes
    
    # Calculer le taux de retard
    taux_retard = 0
    if total_emprunts_actifs > 0:
        taux_retard = (total_emprunts_retard / total_emprunts_actifs) * 100
    
    # Calculer le taux d'utilisation des livres
    taux_utilisation = 0
    if total_livres > 0:
        livres_empruntes = total_livres - total_livres_disponibles
        taux_utilisation = (livres_empruntes / total_livres) * 100
    
    # Livres les plus populaires
    livres_populaires_data = emprunt_service.get_livres_populaires(limit=10)
    popular_books = [
        {
            'book_id': livre['id'],
            'title': livre['titre'],
            'author': livre['auteur'],
            'isbn': livre['isbn'],
            'loan_count': livre['nombre_emprunts']
        }
        for livre in livres_populaires_data
    ]
    
    # Statistiques par rôle d'utilisateur
    stats_emprunts_par_role = emprunt_service.get_statistiques_par_role()
    loans_by_role = [
        {
            'role': stat['role'],
            'total_loans': stat['nombre_emprunts'],
            'active_loans': stat['emprunts_actifs'],
            'overdue_loans': stat['emprunts_retard']
        }
        for stat in stats_emprunts_par_role
    ]
    
    return jsonify({
        'total_books': total_livres,
        'available_books': total_livres_disponibles,
        'total_users': total_users,
        'users_by_role': users_par_role,
        'active_loans': total_emprunts_actifs,
        'returned_loans': total_emprunts_retournes,
        'total_loans': total_emprunts_total,
        'overdue_loans': total_emprunts_retard,
        'overdue_rate': round(taux_retard, 2),
        'utilization_rate': round(taux_utilisation, 2),
        'popular_books': popular_books,
        'loans_by_role': loans_by_role
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


@dashboard_bp.route('/stats/monthly', methods=['GET'])
@require_role(Role.BIBLIOTHECAIRE)
def get_monthly_stats(utilisateur):
    """Récupérer les statistiques mensuelles (Bibliothécaire uniquement)"""
    emprunt_service = EmpruntService()
    
    mois = 12  # Par défaut, 12 derniers mois
    stats_mensuelles = emprunt_service.get_statistiques_par_mois(mois)
    
    return jsonify({
        'monthly_stats': [
            {
                'month': stat['mois'],
                'loan_count': stat['nombre_emprunts']
            }
            for stat in stats_mensuelles
        ]
    }), 200


@dashboard_bp.route('/stats/authors', methods=['GET'])
@require_role(Role.BIBLIOTHECAIRE)
def get_popular_authors(utilisateur):
    """Récupérer les auteurs les plus populaires (Bibliothécaire uniquement)"""
    emprunt_service = EmpruntService()
    
    limit = 10  # Par défaut, top 10
    auteurs_populaires = emprunt_service.get_auteurs_populaires(limit)
    
    return jsonify({
        'popular_authors': [
            {
                'author': auteur['auteur'],
                'loan_count': auteur['nombre_emprunts'],
                'book_count': auteur['nombre_livres']
            }
            for auteur in auteurs_populaires
        ]
    }), 200

