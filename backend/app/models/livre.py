"""
Modèle de données pour les livres
"""


class Livre:
    """Représente un livre dans la bibliothèque"""
    
    def __init__(self, id=None, titre=None, auteur=None, isbn=None, 
                 nombre_exemplaires=None, exemplaires_disponibles=None):
        self.id = id
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.nombre_exemplaires = nombre_exemplaires
        self.exemplaires_disponibles = exemplaires_disponibles
    
    def to_dict(self):
        """Convertir l'objet en dictionnaire"""
        return {
            'id': self.id,
            'titre': self.titre,
            'auteur': self.auteur,
            'isbn': self.isbn,
            'nombre_exemplaires': self.nombre_exemplaires,
            'exemplaires_disponibles': self.exemplaires_disponibles,
            'disponible': self.exemplaires_disponibles > 0 if self.exemplaires_disponibles else False
        }
    
    @staticmethod
    def from_dict(data):
        """Créer un objet Livre depuis un dictionnaire"""
        return Livre(
            id=data.get('id'),
            titre=data.get('titre'),
            auteur=data.get('auteur'),
            isbn=data.get('isbn'),
            nombre_exemplaires=data.get('nombre_exemplaires'),
            exemplaires_disponibles=data.get('exemplaires_disponibles')
        )

