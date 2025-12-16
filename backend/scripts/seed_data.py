"""
Script pour peupler la base de données avec des données de test
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Database
from app.services.livre_service import LivreService
from app.services.utilisateur_service import UtilisateurService
from app.services.emprunt_service import EmpruntService
from app.models.utilisateur import Role

# Données de test
LIVRES = [
    {"titre": "Harry Potter à l'école des sorciers", "auteur": "J.K. Rowling", "isbn": "978-2070584628", "exemplaires": 5},
    {"titre": "Le Seigneur des Anneaux : La Communauté de l'Anneau", "auteur": "J.R.R. Tolkien", "isbn": "978-2266286268", "exemplaires": 3},
    {"titre": "1984", "auteur": "George Orwell", "isbn": "978-2070368228", "exemplaires": 4},
    {"titre": "Le Petit Prince", "auteur": "Antoine de Saint-Exupéry", "isbn": "978-2070612758", "exemplaires": 6},
    {"titre": "L'Étranger", "auteur": "Albert Camus", "isbn": "978-2070360024", "exemplaires": 4},
    {"titre": "Dune", "auteur": "Frank Herbert", "isbn": "978-2266283045", "exemplaires": 3},
    {"titre": "Les Misérables", "auteur": "Albert Camus", "isbn": "978-2070368229", "exemplaires": 2},
    {"titre": "Le Rouge et le Noir", "auteur": "Stendhal", "isbn": "978-2070413119", "exemplaires": 3},
    {"titre": "Madame Bovary", "auteur": "Stendhal", "isbn": "978-2070413118", "exemplaires": 2},
    {"titre": "Germinal", "auteur": "Victor Hugo", "isbn": "978-2070413117", "exemplaires": 3},
    {"titre": "Python pour les Nuls", "auteur": "John Paul Mueller", "isbn": "978-2412050529", "exemplaires": 2},
    {"titre": "Clean Code", "auteur": "Robert C. Martin", "isbn": "978-0132350884", "exemplaires": 2},
    {"titre": "Design Patterns", "auteur": "Erich Gamma", "isbn": "978-0201633610", "exemplaires": 1},
    {"titre": "Introduction to Algorithms", "auteur": "Thomas H. Cormen", "isbn": "978-0262033848", "exemplaires": 1},
    {"titre": "The Pragmatic Programmer", "auteur": "Andrew Hunt", "isbn": "978-0201616224", "exemplaires": 2}
]

UTILISATEURS = [
    {"nom": "Jean Dupont", "email": "jean.dupont@example.com", "password": "password123", "role": Role.ETUDIANT},
    {"nom": "Marie Martin", "email": "marie.marie@example.com", "password": "password123", "role": Role.ETUDIANT},
    {"nom": "Pierre Durand", "email": "pierre.dupont@example.com", "password": "password123", "role": Role.ENSEIGNANT},
    {"nom": "Sophie Lefebvre", "email": "sophie.lefebvre@example.com", "password": "password123", "role": Role.ENSEIGNANT},
    {"nom": "Admin Bibli", "email": "admin@biblio.com", "password": "adminpassword", "role": Role.BIBLIOTHECAIRE},
    {"nom": "Lucie Dubois", "email": "lucie.dubois@example.com", "password": "password123", "role": Role.BIBLIOTHECAIRE}
]

def seed_database():
    print("Démarrage du peuplement de la base de données...")
    
    livre_service = LivreService()
    utilisateur_service = UtilisateurService()
    emprunt_service = EmpruntService()
    
    # Création des utilisateurs
    users = []
    for user_data in UTILISATEURS:
        existing = utilisateur_service.get_by_email(user_data["email"])
        if not existing:
            user = utilisateur_service.create(
                nom=user_data["nom"],
                email=user_data["email"],
                mot_de_passe=user_data["password"],
                role=user_data["role"]
            )
            users.append(user)
            print(f"Utilisateur créé : {user.nom} ({user.role})")
        else:
            users.append(existing)
            print(f"Utilisateur existant : {existing.nom}")
            
    # Création des livres
    livres = []
    for livre_data in LIVRES:
        # Vérifier si le livre existe déjà (par ISBN ou titre)
        # Ici on simplifie en créant toujours (attention aux doublons si réexécuté sans check)
        livre = livre_service.create(
            titre=livre_data["titre"],
            auteur=livre_data["auteur"],
            isbn=livre_data["isbn"],
            nombre_exemplaires=livre_data["exemplaires"]
        )
        livres.append(livre)
        print(f"Livre créé : {livre.titre}")
        
    # Création d'emprunts aléatoires
    # Emprunts en cours
    for _ in range(15):
        livre = random.choice(livres)
        user = random.choice(users)
        
        # Vérifier disponibilité
        if livre.exemplaires_disponibles > 0:
            emprunt = emprunt_service.create(livre.id, user.id)
            # Mettre à jour la date pour simuler des emprunts passés
            days_ago = random.randint(1, 60)
            date_emprunt = datetime.now() - timedelta(days=days_ago)
            date_retour_prevue = date_emprunt + timedelta(days=30)
            
            # Mise à jour manuelle en SQL pour changer les dates
            query = "UPDATE emprunts SET date_emprunt = %s, date_retour_prevue = %s WHERE id = %s"
            emprunt_service.db.execute_query(query, (date_emprunt, date_retour_prevue, emprunt.id))
            emprunt_service.db.commit()
            
            # Décrémenter exemplaires
            livre_service.decrementer_exemplaires_disponibles(livre.id)
            # Mettre à jour l'objet livre local
            livre.exemplaires_disponibles -= 1
            
            print(f"Emprunt créé : {livre.titre} par {user.nom} (il y a {days_ago} jours)")
            
    # Emprunts retournés
    for _ in range(10):
        livre = random.choice(livres)
        user = random.choice(users)
        
        if livre.exemplaires_disponibles > 0:
            emprunt = emprunt_service.create(livre.id, user.id)
            
            # Dates passées
            days_ago = random.randint(30, 90)
            date_emprunt = datetime.now() - timedelta(days=days_ago)
            date_retour_prevue = date_emprunt + timedelta(days=30)
            date_retour_reelle = date_emprunt + timedelta(days=random.randint(5, 35))
            
            # Mise à jour SQL
            query = """
                UPDATE emprunts 
                SET date_emprunt = %s, date_retour_prevue = %s, date_retour_reelle = %s, statut = 'retourne' 
                WHERE id = %s
            """
            emprunt_service.db.execute_query(query, (date_emprunt, date_retour_prevue, date_retour_reelle, emprunt.id))
            emprunt_service.db.commit()
            
            # Pas besoin de décrémenter car retourné (ou plutôt on décrémente puis incrémente, donc neutre)
            # Mais create() ne décrémente pas automatiquement dans le service actuel, c'est fait dans le contrôleur
            # Donc ici on ne fait rien sur les exemplaires
            
            print(f"Emprunt retourné créé : {livre.titre} par {user.nom}")

    # Mettre à jour les statuts en retard
    emprunt_service.update_statut_retard()
    print("Statuts de retard mis à jour.")
    
    print("Peuplement terminé !")

if __name__ == "__main__":
    seed_database()

