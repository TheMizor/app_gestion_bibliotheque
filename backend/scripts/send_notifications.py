#!/usr/bin/env python3
"""
Script pour exécuter manuellement les notifications
Utile pour les tests ou l'exécution via cron
"""
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.notification_service import NotificationService
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("Démarrage du traitement des notifications...")
    
    notification_service = NotificationService()
    resultats = notification_service.traiter_toutes_notifications()
    
    print("\n=== Résultats ===")
    print(f"Rappels J-30 envoyés: {resultats['rappels_30_jours']}")
    print(f"Rappels J-5 envoyés: {resultats['rappels_5_jours']}")
    print(f"Notifications de retard envoyées: {resultats['notifications_retard']}")
    print(f"Timestamp: {resultats['timestamp']}")
    print("\nTraitement terminé.")

