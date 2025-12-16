"""
Service de gestion des livres
"""
from datetime import datetime
from app.database import Database
from app.models.livre import Livre


class LivreService:
    """Service pour les opérations CRUD sur les livres"""
    
    def __init__(self):
        self.db = Database()
    
    def create(self, titre, auteur, isbn=None, nombre_exemplaires=1):
        """Créer un nouveau livre"""
        query = """
            INSERT INTO livres (titre, auteur, isbn, nombre_exemplaires, exemplaires_disponibles)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (titre, auteur, isbn, nombre_exemplaires, nombre_exemplaires)
        
        cursor = self.db.execute_query(query, params)
        livre_id = cursor.lastrowid
        self.db.commit()
        cursor.close()
        
        return self.get_by_id(livre_id)
    
    def get_by_id(self, livre_id):
        """Récupérer un livre par son ID"""
        query = "SELECT * FROM livres WHERE id = %s"
        cursor = self.db.execute_query(query, (livre_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return Livre.from_dict(result)
        return None
    
    def get_all(self, page=1, limit=20, search=None, available_only=False):
        """Récupérer tous les livres avec pagination et filtres"""
        offset = (page - 1) * limit
        conditions = []
        params = []
        
        if search:
            conditions.append("(titre LIKE %s OR auteur LIKE %s)")
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern])
        
        if available_only:
            conditions.append("exemplaires_disponibles > 0")
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # Requête pour récupérer les livres
        query = f"SELECT * FROM livres{where_clause} ORDER BY titre LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor = self.db.execute_query(query, params)
        livres = [Livre.from_dict(row) for row in cursor.fetchall()]
        cursor.close()
        
        # Requête pour compter le total
        count_query = f"SELECT COUNT(*) as total FROM livres{where_clause}"
        count_params = params[:-2]  # Enlever limit et offset
        cursor = self.db.execute_query(count_query, count_params)
        total = cursor.fetchone()['total']
        cursor.close()
        
        return {
            'livres': livres,
            'total': total,
            'page': page,
            'limit': limit
        }
    
    def update(self, livre_id, titre=None, auteur=None, isbn=None, nombre_exemplaires=None):
        """Mettre à jour un livre"""
        updates = []
        params = []
        
        if titre is not None:
            updates.append("titre = %s")
            params.append(titre)
        if auteur is not None:
            updates.append("auteur = %s")
            params.append(auteur)
        if isbn is not None:
            updates.append("isbn = %s")
            params.append(isbn)
        if nombre_exemplaires is not None:
            # Ajuster les exemplaires disponibles si nécessaire
            livre = self.get_by_id(livre_id)
            if livre:
                diff = nombre_exemplaires - livre.nombre_exemplaires
                updates.append("nombre_exemplaires = %s")
                params.append(nombre_exemplaires)
                updates.append("exemplaires_disponibles = exemplaires_disponibles + %s")
                params.append(diff)
        
        if not updates:
            return self.get_by_id(livre_id)
        
        params.append(livre_id)
        query = f"UPDATE livres SET {', '.join(updates)} WHERE id = %s"
        
        cursor = self.db.execute_query(query, params)
        self.db.commit()
        cursor.close()
        
        return self.get_by_id(livre_id)
    
    def delete(self, livre_id):
        """Supprimer un livre"""
        query = "DELETE FROM livres WHERE id = %s"
        cursor = self.db.execute_query(query, (livre_id,))
        self.db.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        
        return deleted
    
    def decrementer_exemplaires_disponibles(self, livre_id):
        """Décrémenter le nombre d'exemplaires disponibles"""
        query = """
            UPDATE livres 
            SET exemplaires_disponibles = exemplaires_disponibles - 1 
            WHERE id = %s AND exemplaires_disponibles > 0
        """
        cursor = self.db.execute_query(query, (livre_id,))
        self.db.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        
        return updated
    
    def incrementer_exemplaires_disponibles(self, livre_id):
        """Incrémenter le nombre d'exemplaires disponibles"""
        query = """
            UPDATE livres 
            SET exemplaires_disponibles = exemplaires_disponibles + 1 
            WHERE id = %s AND exemplaires_disponibles < nombre_exemplaires
        """
        cursor = self.db.execute_query(query, (livre_id,))
        self.db.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        
        return updated

