"""
Routes pour la gestion manuelle des notifications (Bibliothécaires uniquement)
"""
from flask import Blueprint, jsonify
from app.services.notification_service import NotificationService
from app.utils.auth import require_role
from app.models.utilisateur import Role

notification_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


@notification_bp.route('/send-30-days', methods=['POST'])
@require_role(Role.BIBLIOTHECAIRE)
def send_30_days_reminders(utilisateur):
    """Envoyer manuellement les rappels J-30 (Bibliothécaire uniquement)"""
    notification_service = NotificationService()
    count = notification_service.traiter_rappels_30_jours()
    
    return jsonify({
        'message': f'{count} rappel(s) J-30 envoyé(s)',
        'count': count
    }), 200


@notification_bp.route('/send-5-days', methods=['POST'])
@require_role(Role.BIBLIOTHECAIRE)
def send_5_days_reminders(utilisateur):
    """Envoyer manuellement les rappels J-5 (Bibliothécaire uniquement)"""
    notification_service = NotificationService()
    count = notification_service.traiter_rappels_5_jours()
    
    return jsonify({
        'message': f'{count} rappel(s) J-5 envoyé(s)',
        'count': count
    }), 200


@notification_bp.route('/send-overdue', methods=['POST'])
@require_role(Role.BIBLIOTHECAIRE)
def send_overdue_notifications(utilisateur):
    """Envoyer manuellement les notifications de retard (Bibliothécaire uniquement)"""
    notification_service = NotificationService()
    count = notification_service.traiter_notifications_retard()
    
    return jsonify({
        'message': f'{count} notification(s) de retard envoyée(s)',
        'count': count
    }), 200


@notification_bp.route('/send-all', methods=['POST'])
@require_role(Role.BIBLIOTHECAIRE)
def send_all_notifications(utilisateur):
    """Envoyer manuellement toutes les notifications (Bibliothécaire uniquement)"""
    notification_service = NotificationService()
    resultats = notification_service.traiter_toutes_notifications()
    
    return jsonify({
        'message': 'Toutes les notifications ont été traitées',
        'results': resultats
    }), 200

