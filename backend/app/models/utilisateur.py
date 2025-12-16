"""
Modèle de données pour les utilisateurs
"""


class Role:
    """Rôles disponibles dans l'application"""
    BIBLIOTHECAIRE = 'bibliothecaire'
    ETUDIANT = 'etudiant'
    ENSEIGNANT = 'enseignant'


class Utilisateur:
    """Représente un utilisateur de la bibliothèque"""
    
    def __init__(self, id=None, nom=None, email=None, mot_de_passe=None, 
                 role=None, date_creation=None):
        self.id = id
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = role
        self.date_creation = date_creation
    
    def to_dict(self):
        """Convertir l'objet en dictionnaire (sans le mot de passe)"""
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email,
            'role': self.role,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }
    
    def is_bibliothecaire(self):
        """Vérifier si l'utilisateur est bibliothécaire"""
        return self.role == Role.BIBLIOTHECAIRE
    
    def can_manage_books(self):
        """Vérifier si l'utilisateur peut gérer les livres"""
        return self.is_bibliothecaire()
    
    def can_view_dashboard(self):
        """Vérifier si l'utilisateur peut voir le tableau de bord"""
        return self.is_bibliothecaire()
    
    @staticmethod
    def from_dict(data):
        """Créer un objet Utilisateur depuis un dictionnaire"""
        return Utilisateur(
            id=data.get('id'),
            nom=data.get('nom'),
            email=data.get('email'),
            mot_de_passe=data.get('mot_de_passe'),
            role=data.get('role'),
            date_creation=data.get('date_creation')
        )

