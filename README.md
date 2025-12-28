# Application de Gestion de Bibliothèque

## Description du Projet

Application web de gestion de bibliothèque universitaire permettant d'améliorer la gestion des livres, des emprunts et des utilisateurs.

## Structure du Projet

```
app_gestion_bibliotheque/
├── backend/          # Backend Python
│   ├── app/         # Code source de l'application
│   ├── tests/       # Tests unitaires
│   └── requirements.txt
├── frontend/        # Frontend React.js
│   ├── src/        # Code source React
│   ├── public/     # Fichiers statiques
│   └── package.json
├── .gitignore      # Fichiers à ignorer par Git
└── README.md       # Ce fichier
```

## Technologies Utilisées

- **Backend** : Python
- **Frontend** : React.js
- **Base de données** : MySQL
- **Gestion de version** : Git

## Fonctionnalités

- ✅ Gestion des livres : Ajout, modification, suppression, recherche et affichage
- ✅ Gestion des emprunts et retours : Suivi des prêts, notifications des retards
- ✅ Authentification et gestion des utilisateurs : Rôles (bibliothécaire, étudiant, enseignant)
- ✅ Tableau de bord : Statistiques sur l'utilisation de la bibliothèque (réservé aux bibliothécaires)
- ✅ Interface utilisateur ergonomique : Accessible via web et mobile

## Installation

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Contributeurs

Projet réalisé par groupe de 3 étudiants maximum.

## Date de Rendu

32/12/2025
64: 
65: ## Utilisateurs de Test
66: 
67: - **Administrateur (Bibliothécaire)** : `admin@biblio.com` / `adminpassword`
68: - **Étudiant** : `jean.dupont@example.com` / `password123`
69: - **Enseignant** : `pierre.dupont@example.com` / `password123`
70:

## Notes

- Respect des bonnes pratiques de développement (modularité, documentation, tests unitaires)
- Gestion des accès et sécurisation des données utilisateurs
- Utilisation de Git pour la gestion de version

