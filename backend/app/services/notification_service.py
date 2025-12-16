"""
Service de gestion des notifications
"""
import logging
from datetime import datetime
from app.services.emprunt_service import EmpruntService
from app.services.utilisateur_service import UtilisateurService

logger = logging.getLogger(__name__)


class NotificationService:
    """Service pour gérer les notifications et rappels"""
    
    def __init__(self):
        self.emprunt_service = EmpruntService()
        self.utilisateur_service = UtilisateurService()
    
    def envoyer_notification_email(self, destinataire_email, sujet, message):
        """
        Envoyer une notification par email
        
        Note: Pour l'instant, cette méthode log simplement le message.
        Dans un environnement de production, intégrer un service d'email
        (SMTP, SendGrid, Mailgun, etc.)
        """
        logger.info(f"Notification envoyée à {destinataire_email}")
        logger.info(f"Sujet: {sujet}")
        logger.info(f"Message: {message}")
        
        # TODO: Implémenter l'envoi réel d'email
        # Exemple avec SMTP:
        # import smtplib
        # from email.mime.text import MIMEText
        # msg = MIMEText(message)
        # msg['Subject'] = sujet
        # msg['From'] = 'bibliotheque@example.com'
        # msg['To'] = destinataire_email
        # server = smtplib.SMTP('smtp.example.com', 587)
        # server.send_message(msg)
        # server.quit()
        
        return True
    
    def envoyer_rappel_30_jours(self, emprunt):
        """Envoyer un rappel à J-30 pour un emprunt"""
        sujet = f"Rappel: Retour de livre prévu dans 30 jours - {emprunt.livre_titre}"
        message = f"""
Bonjour {emprunt.utilisateur_nom},

Ceci est un rappel automatique concernant votre emprunt de livre.

Livre: {emprunt.livre_titre}
Date d'emprunt: {emprunt.date_emprunt}
Date de retour prévue: {emprunt.date_retour_prevue}

Votre livre doit être retourné dans 30 jours.

Merci de votre attention.

Cordialement,
L'équipe de la bibliothèque universitaire
        """
        
        return self.envoyer_notification_email(
            emprunt.utilisateur_email,
            sujet,
            message.strip()
        )
    
    def envoyer_rappel_5_jours(self, emprunt):
        """Envoyer un rappel à J-5 pour un emprunt"""
        sujet = f"Rappel urgent: Retour de livre prévu dans 5 jours - {emprunt.livre_titre}"
        message = f"""
Bonjour {emprunt.utilisateur_nom},

Ceci est un rappel urgent concernant votre emprunt de livre.

Livre: {emprunt.livre_titre}
Date d'emprunt: {emprunt.date_emprunt}
Date de retour prévue: {emprunt.date_retour_prevue}

⚠️ Votre livre doit être retourné dans 5 jours.

Merci de retourner le livre à temps pour éviter des frais de retard.

Cordialement,
L'équipe de la bibliothèque universitaire
        """
        
        return self.envoyer_notification_email(
            emprunt.utilisateur_email,
            sujet,
            message.strip()
        )
    
    def envoyer_notification_retard(self, emprunt):
        """Envoyer une notification pour un emprunt en retard"""
        jours_retard = abs(emprunt.calculer_jours_restants()) if emprunt.calculer_jours_restants() else 0
        
        sujet = f"⚠️ Retard: Livre non retourné - {emprunt.livre_titre}"
        message = f"""
Bonjour {emprunt.utilisateur_nom},

Ceci est une notification concernant votre emprunt de livre en retard.

Livre: {emprunt.livre_titre}
Date d'emprunt: {emprunt.date_emprunt}
Date de retour prévue: {emprunt.date_retour_prevue}
Jours de retard: {jours_retard}

⚠️ Votre livre est en retard de {jours_retard} jour(s).

Merci de retourner le livre dès que possible.

Cordialement,
L'équipe de la bibliothèque universitaire
        """
        
        return self.envoyer_notification_email(
            emprunt.utilisateur_email,
            sujet,
            message.strip()
        )
    
    def traiter_rappels_30_jours(self):
        """Traiter tous les rappels à J-30"""
        emprunts = self.emprunt_service.get_rappels_30_jours()
        notifications_envoyees = 0
        
        for emprunt in emprunts:
            try:
                if self.envoyer_rappel_30_jours(emprunt):
                    notifications_envoyees += 1
                    logger.info(f"Rappel J-30 envoyé pour l'emprunt {emprunt.id}")
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi du rappel J-30 pour l'emprunt {emprunt.id}: {e}")
        
        return notifications_envoyees
    
    def traiter_rappels_5_jours(self):
        """Traiter tous les rappels à J-5"""
        emprunts = self.emprunt_service.get_rappels_5_jours()
        notifications_envoyees = 0
        
        for emprunt in emprunts:
            try:
                if self.envoyer_rappel_5_jours(emprunt):
                    notifications_envoyees += 1
                    logger.info(f"Rappel J-5 envoyé pour l'emprunt {emprunt.id}")
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi du rappel J-5 pour l'emprunt {emprunt.id}: {e}")
        
        return notifications_envoyees
    
    def traiter_notifications_retard(self):
        """Traiter toutes les notifications de retard"""
        # Mettre à jour les statuts en retard
        self.emprunt_service.update_statut_retard()
        
        emprunts = self.emprunt_service.get_emprunts_en_retard()
        notifications_envoyees = 0
        
        for emprunt in emprunts:
            try:
                if self.envoyer_notification_retard(emprunt):
                    notifications_envoyees += 1
                    logger.info(f"Notification de retard envoyée pour l'emprunt {emprunt.id}")
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi de la notification de retard pour l'emprunt {emprunt.id}: {e}")
        
        return notifications_envoyees
    
    def traiter_toutes_notifications(self):
        """Traiter toutes les notifications (rappels et retards)"""
        logger.info("Début du traitement des notifications")
        
        resultats = {
            'rappels_30_jours': 0,
            'rappels_5_jours': 0,
            'notifications_retard': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            resultats['rappels_30_jours'] = self.traiter_rappels_30_jours()
        except Exception as e:
            logger.error(f"Erreur lors du traitement des rappels J-30: {e}")
        
        try:
            resultats['rappels_5_jours'] = self.traiter_rappels_5_jours()
        except Exception as e:
            logger.error(f"Erreur lors du traitement des rappels J-5: {e}")
        
        try:
            resultats['notifications_retard'] = self.traiter_notifications_retard()
        except Exception as e:
            logger.error(f"Erreur lors du traitement des notifications de retard: {e}")
        
        logger.info(f"Traitement terminé: {resultats}")
        return resultats

