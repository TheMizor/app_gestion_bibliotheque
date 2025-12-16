"""
Modèle de données pour les emprunts
"""
from datetime import datetime, timedelta


class StatutEmprunt:
    """Statuts possibles d'un emprunt"""
    ACTIF = 'actif'
    RETOURNE = 'retourne'
    EN_RETARD = 'en_retard'


class Emprunt:
    """Représente un emprunt de livre"""
    
    def __init__(self, id=None, livre_id=None, utilisateur_id=None, 
                 date_emprunt=None, date_retour_prevue=None, 
                 date_retour_reelle=None, statut=None):
        self.id = id
        self.livre_id = livre_id
        self.utilisateur_id = utilisateur_id
        self.date_emprunt = date_emprunt
        self.date_retour_prevue = date_retour_prevue
        self.date_retour_reelle = date_retour_reelle
        self.statut = statut or StatutEmprunt.ACTIF
    
    def calculer_jours_restants(self):
        """Calculer le nombre de jours restants avant la date de retour"""
        if not self.date_retour_prevue:
            return None
        
        if isinstance(self.date_retour_prevue, str):
            date_retour = datetime.fromisoformat(self.date_retour_prevue)
        else:
            date_retour = self.date_retour_prevue
        
        jours_restants = (date_retour - datetime.now()).days
        return jours_restants
    
    def est_en_retard(self):
        """Vérifier si l'emprunt est en retard"""
        jours_restants = self.calculer_jours_restants()
        return jours_restants is not None and jours_restants < 0
    
    def necessite_rappel_30_jours(self):
        """Vérifier si un rappel à J-30 est nécessaire"""
        jours_restants = self.calculer_jours_restants()
        return jours_restants == 30
    
    def necessite_rappel_5_jours(self):
        """Vérifier si un rappel à J-5 est nécessaire"""
        jours_restants = self.calculer_jours_restants()
        return jours_restants == 5
    
    def to_dict(self):
        """Convertir l'objet en dictionnaire"""
        jours_restants = self.calculer_jours_restants()
        return {
            'id': self.id,
            'livre_id': self.livre_id,
            'utilisateur_id': self.utilisateur_id,
            'date_emprunt': self.date_emprunt.isoformat() if isinstance(self.date_emprunt, datetime) else self.date_emprunt,
            'date_retour_prevue': self.date_retour_prevue.isoformat() if isinstance(self.date_retour_prevue, datetime) else self.date_retour_prevue,
            'date_retour_reelle': self.date_retour_reelle.isoformat() if isinstance(self.date_retour_reelle, datetime) else self.date_retour_reelle,
            'statut': self.statut,
            'jours_restants': jours_restants,
            'en_retard': self.est_en_retard()
        }
    
    @staticmethod
    def from_dict(data):
        """Créer un objet Emprunt depuis un dictionnaire"""
        return Emprunt(
            id=data.get('id'),
            livre_id=data.get('livre_id'),
            utilisateur_id=data.get('utilisateur_id'),
            date_emprunt=data.get('date_emprunt'),
            date_retour_prevue=data.get('date_retour_prevue'),
            date_retour_reelle=data.get('date_retour_reelle'),
            statut=data.get('statut')
        )

