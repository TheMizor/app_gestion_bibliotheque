"""
Système de planification des tâches pour les notifications
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """Gestionnaire de planification des notifications"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.notification_service = NotificationService()
    
    def demarrer(self):
        """Démarrer le planificateur de tâches"""
        # Vérifier les rappels J-30 et J-5 tous les jours à 9h00
        self.scheduler.add_job(
            func=self.notification_service.traiter_rappels_30_jours,
            trigger=CronTrigger(hour=9, minute=0),
            id='rappels_30_jours',
            name='Rappels J-30',
            replace_existing=True
        )
        
        self.scheduler.add_job(
            func=self.notification_service.traiter_rappels_5_jours,
            trigger=CronTrigger(hour=9, minute=0),
            id='rappels_5_jours',
            name='Rappels J-5',
            replace_existing=True
        )
        
        # Vérifier les retards tous les jours à 10h00
        self.scheduler.add_job(
            func=self.notification_service.traiter_notifications_retard,
            trigger=CronTrigger(hour=10, minute=0),
            id='notifications_retard',
            name='Notifications de retard',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Planificateur de notifications démarré")
    
    def arreter(self):
        """Arrêter le planificateur de tâches"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Planificateur de notifications arrêté")
    
    def executer_manuellement(self):
        """Exécuter manuellement toutes les notifications (pour tests)"""
        return self.notification_service.traiter_toutes_notifications()

