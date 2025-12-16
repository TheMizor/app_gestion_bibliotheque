"""
Service de gestion des emprunts
"""
from datetime import datetime, timedelta
from app.database import Database
from app.models.emprunt import Emprunt, StatutEmprunt


class EmpruntService:
    """Service pour les opérations CRUD sur les emprunts"""
    
    def __init__(self):
        self.db = Database()
    
    def create(self, livre_id, utilisateur_id, duree_jours=30):
        """Créer un nouvel emprunt"""
        date_emprunt = datetime.now()
        date_retour_prevue = date_emprunt + timedelta(days=duree_jours)
        
        query = """
            INSERT INTO emprunts (livre_id, utilisateur_id, date_emprunt, date_retour_prevue, statut)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (livre_id, utilisateur_id, date_emprunt, date_retour_prevue, StatutEmprunt.ACTIF)
        
        cursor = self.db.execute_query(query, params)
        emprunt_id = cursor.lastrowid
        self.db.commit()
        cursor.close()
        
        return self.get_by_id(emprunt_id)
    
    def get_by_id(self, emprunt_id):
        """Récupérer un emprunt par son ID avec détails du livre et utilisateur"""
        query = """
            SELECT e.*, 
                   l.titre as livre_titre, l.auteur as livre_auteur,
                   u.nom as utilisateur_nom, u.email as utilisateur_email
            FROM emprunts e
            LEFT JOIN livres l ON e.livre_id = l.id
            LEFT JOIN utilisateurs u ON e.utilisateur_id = u.id
            WHERE e.id = %s
        """
        cursor = self.db.execute_query(query, (emprunt_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            emprunt = Emprunt.from_dict(result)
            # Ajouter les informations supplémentaires
            emprunt.livre_titre = result.get('livre_titre')
            emprunt.livre_auteur = result.get('livre_auteur')
            emprunt.utilisateur_nom = result.get('utilisateur_nom')
            emprunt.utilisateur_email = result.get('utilisateur_email')
            return emprunt
        return None
    
    def get_all(self, page=1, limit=20, utilisateur_id=None, statut=None, livre_id=None):
        """Récupérer tous les emprunts avec pagination et filtres"""
        offset = (page - 1) * limit
        conditions = []
        params = []
        
        if utilisateur_id:
            conditions.append("e.utilisateur_id = %s")
            params.append(utilisateur_id)
        if statut:
            conditions.append("e.statut = %s")
            params.append(statut)
        if livre_id:
            conditions.append("e.livre_id = %s")
            params.append(livre_id)
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        query = f"""
            SELECT e.*, 
                   l.titre as livre_titre, l.auteur as livre_auteur,
                   u.nom as utilisateur_nom, u.email as utilisateur_email
            FROM emprunts e
            LEFT JOIN livres l ON e.livre_id = l.id
            LEFT JOIN utilisateurs u ON e.utilisateur_id = u.id
            {where_clause}
            ORDER BY e.date_emprunt DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        cursor = self.db.execute_query(query, params)
        results = cursor.fetchall()
        cursor.close()
        
        emprunts = []
        for row in results:
            emprunt = Emprunt.from_dict(row)
            emprunt.livre_titre = row.get('livre_titre')
            emprunt.livre_auteur = row.get('livre_auteur')
            emprunt.utilisateur_nom = row.get('utilisateur_nom')
            emprunt.utilisateur_email = row.get('utilisateur_email')
            emprunts.append(emprunt)
        
        # Compter le total
        count_query = f"SELECT COUNT(*) as total FROM emprunts e{where_clause}"
        count_params = params[:-2]
        cursor = self.db.execute_query(count_query, count_params)
        total = cursor.fetchone()['total']
        cursor.close()
        
        return {
            'emprunts': emprunts,
            'total': total,
            'page': page,
            'limit': limit
        }
    
    def retourner(self, emprunt_id):
        """Retourner un livre emprunté"""
        date_retour = datetime.now()
        
        query = """
            UPDATE emprunts 
            SET date_retour_reelle = %s, statut = %s
            WHERE id = %s AND statut = %s
        """
        params = (date_retour, StatutEmprunt.RETOURNE, emprunt_id, StatutEmprunt.ACTIF)
        
        cursor = self.db.execute_query(query, params)
        self.db.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        
        if updated:
            return self.get_by_id(emprunt_id)
        return None
    
    def update_statut_retard(self):
        """Mettre à jour le statut des emprunts en retard"""
        query = """
            UPDATE emprunts 
            SET statut = %s
            WHERE statut = %s 
            AND date_retour_prevue < NOW()
        """
        cursor = self.db.execute_query(query, (StatutEmprunt.EN_RETARD, StatutEmprunt.ACTIF))
        self.db.commit()
        updated = cursor.rowcount
        cursor.close()
        
        return updated
    
    def get_emprunts_actifs_utilisateur(self, utilisateur_id):
        """Récupérer tous les emprunts actifs d'un utilisateur"""
        return self.get_all(utilisateur_id=utilisateur_id, statut=StatutEmprunt.ACTIF)
    
    def get_emprunts_en_retard(self):
        """Récupérer tous les emprunts en retard"""
        return self.get_all(statut=StatutEmprunt.EN_RETARD)
    
    def get_rappels_30_jours(self):
        """Récupérer les emprunts nécessitant un rappel à J-30"""
        query = """
            SELECT e.*, 
                   l.titre as livre_titre,
                   u.nom as utilisateur_nom, u.email as utilisateur_email
            FROM emprunts e
            LEFT JOIN livres l ON e.livre_id = l.id
            LEFT JOIN utilisateurs u ON e.utilisateur_id = u.id
            WHERE e.statut = %s
            AND DATEDIFF(e.date_retour_prevue, NOW()) = 30
        """
        cursor = self.db.execute_query(query, (StatutEmprunt.ACTIF,))
        results = cursor.fetchall()
        cursor.close()
        
        emprunts = []
        for row in results:
            emprunt = Emprunt.from_dict(row)
            emprunt.livre_titre = row.get('livre_titre')
            emprunt.utilisateur_nom = row.get('utilisateur_nom')
            emprunt.utilisateur_email = row.get('utilisateur_email')
            emprunts.append(emprunt)
        
        return emprunts
    
    def get_rappels_5_jours(self):
        """Récupérer les emprunts nécessitant un rappel à J-5"""
        query = """
            SELECT e.*, 
                   l.titre as livre_titre,
                   u.nom as utilisateur_nom, u.email as utilisateur_email
            FROM emprunts e
            LEFT JOIN livres l ON e.livre_id = l.id
            LEFT JOIN utilisateurs u ON e.utilisateur_id = u.id
            WHERE e.statut = %s
            AND DATEDIFF(e.date_retour_prevue, NOW()) = 5
        """
        cursor = self.db.execute_query(query, (StatutEmprunt.ACTIF,))
        results = cursor.fetchall()
        cursor.close()
        
        emprunts = []
        for row in results:
            emprunt = Emprunt.from_dict(row)
            emprunt.livre_titre = row.get('livre_titre')
            emprunt.utilisateur_nom = row.get('utilisateur_nom')
            emprunt.utilisateur_email = row.get('utilisateur_email')
            emprunts.append(emprunt)
        
        return emprunts
    
    def get_livres_populaires(self, limit=10):
        """Récupérer les livres les plus populaires (basés sur le nombre d'emprunts)"""
        query = """
            SELECT 
                l.id,
                l.titre,
                l.auteur,
                l.isbn,
                COUNT(e.id) as nombre_emprunts
            FROM livres l
            LEFT JOIN emprunts e ON l.id = e.livre_id
            GROUP BY l.id, l.titre, l.auteur, l.isbn
            ORDER BY nombre_emprunts DESC
            LIMIT %s
        """
        cursor = self.db.execute_query(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def get_statistiques_par_role(self):
        """Récupérer les statistiques d'emprunts par rôle d'utilisateur"""
        query = """
            SELECT 
                u.role,
                COUNT(e.id) as nombre_emprunts,
                COUNT(CASE WHEN e.statut = 'actif' THEN 1 END) as emprunts_actifs,
                COUNT(CASE WHEN e.statut = 'en_retard' THEN 1 END) as emprunts_retard
            FROM utilisateurs u
            LEFT JOIN emprunts e ON u.id = e.utilisateur_id
            GROUP BY u.role
        """
        cursor = self.db.execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def get_statistiques_par_mois(self, mois=12):
        """Récupérer les statistiques d'emprunts par mois"""
        query = """
            SELECT 
                DATE_FORMAT(date_emprunt, '%%Y-%%m') as mois,
                COUNT(*) as nombre_emprunts
            FROM emprunts
            WHERE date_emprunt >= DATE_SUB(NOW(), INTERVAL %s MONTH)
            GROUP BY DATE_FORMAT(date_emprunt, '%%Y-%%m')
            ORDER BY mois DESC
        """
        cursor = self.db.execute_query(query, (mois,))
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def get_auteurs_populaires(self, limit=10):
        """Récupérer les auteurs les plus empruntés"""
        query = """
            SELECT 
                l.auteur,
                COUNT(e.id) as nombre_emprunts,
                COUNT(DISTINCT l.id) as nombre_livres
            FROM livres l
            LEFT JOIN emprunts e ON l.id = e.livre_id
            WHERE l.auteur IS NOT NULL
            GROUP BY l.auteur
            ORDER BY nombre_emprunts DESC
            LIMIT %s
        """
        cursor = self.db.execute_query(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        
        return results

