"""
Service de gestion des utilisateurs
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import Database
from app.models.utilisateur import Utilisateur, Role


class UtilisateurService:
    """Service pour les opérations CRUD sur les utilisateurs"""
    
    def __init__(self):
        self.db = Database()
    
    def create(self, nom, email, mot_de_passe, role=Role.ETUDIANT):
        """Créer un nouvel utilisateur"""
        # Vérifier si l'email existe déjà
        if self.get_by_email(email):
            return None
        
        # Hasher le mot de passe
        mot_de_passe_hash = generate_password_hash(mot_de_passe)
        
        query = """
            INSERT INTO utilisateurs (nom, email, mot_de_passe, role)
            VALUES (%s, %s, %s, %s)
        """
        params = (nom, email, mot_de_passe_hash, role)
        
        cursor = self.db.execute_query(query, params)
        utilisateur_id = cursor.lastrowid
        self.db.commit()
        cursor.close()
        
        return self.get_by_id(utilisateur_id)
    
    def get_by_id(self, utilisateur_id):
        """Récupérer un utilisateur par son ID"""
        query = "SELECT * FROM utilisateurs WHERE id = %s"
        cursor = self.db.execute_query(query, (utilisateur_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return Utilisateur.from_dict(result)
        return None
    
    def get_by_email(self, email):
        """Récupérer un utilisateur par son email"""
        query = "SELECT * FROM utilisateurs WHERE email = %s"
        cursor = self.db.execute_query(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return Utilisateur.from_dict(result)
        return None
    
    def get_all(self, page=1, limit=20, role=None):
        """Récupérer tous les utilisateurs avec pagination"""
        offset = (page - 1) * limit
        conditions = []
        params = []
        
        if role:
            conditions.append("role = %s")
            params.append(role)
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        query = f"SELECT * FROM utilisateurs{where_clause} ORDER BY nom LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor = self.db.execute_query(query, params)
        utilisateurs = [Utilisateur.from_dict(row) for row in cursor.fetchall()]
        cursor.close()
        
        # Compter le total
        count_query = f"SELECT COUNT(*) as total FROM utilisateurs{where_clause}"
        count_params = params[:-2]
        cursor = self.db.execute_query(count_query, count_params)
        total = cursor.fetchone()['total']
        cursor.close()
        
        return {
            'utilisateurs': utilisateurs,
            'total': total,
            'page': page,
            'limit': limit
        }
    
    def update(self, utilisateur_id, nom=None, email=None, mot_de_passe=None, role=None):
        """Mettre à jour un utilisateur"""
        updates = []
        params = []
        
        if nom is not None:
            updates.append("nom = %s")
            params.append(nom)
        if email is not None:
            # Vérifier que l'email n'est pas déjà utilisé
            existing = self.get_by_email(email)
            if existing and existing.id != utilisateur_id:
                return None
            updates.append("email = %s")
            params.append(email)
        if mot_de_passe is not None:
            updates.append("mot_de_passe = %s")
            params.append(generate_password_hash(mot_de_passe))
        if role is not None:
            updates.append("role = %s")
            params.append(role)
        
        if not updates:
            return self.get_by_id(utilisateur_id)
        
        params.append(utilisateur_id)
        query = f"UPDATE utilisateurs SET {', '.join(updates)} WHERE id = %s"
        
        cursor = self.db.execute_query(query, params)
        self.db.commit()
        cursor.close()
        
        return self.get_by_id(utilisateur_id)
    
    def delete(self, utilisateur_id):
        """Supprimer un utilisateur"""
        query = "DELETE FROM utilisateurs WHERE id = %s"
        cursor = self.db.execute_query(query, (utilisateur_id,))
        self.db.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        
        return deleted
    
    def verify_password(self, utilisateur, mot_de_passe):
        """Vérifier le mot de passe d'un utilisateur"""
        if not utilisateur:
            return False
        
        # Récupérer le hash depuis la base de données
        query = "SELECT mot_de_passe FROM utilisateurs WHERE id = %s"
        cursor = self.db.execute_query(query, (utilisateur.id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return check_password_hash(result['mot_de_passe'], mot_de_passe)
        return False

