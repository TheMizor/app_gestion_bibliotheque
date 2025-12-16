# Frontend - Application de Gestion de Bibliothèque

## Description

Frontend développé en React.js pour l'interface utilisateur de la gestion de bibliothèque universitaire.

## Structure du projet

```
frontend/
├── public/
│   └── index.html          # Template HTML principal
├── src/
│   ├── components/         # Composants React réutilisables
│   ├── pages/              # Pages de l'application
│   │   ├── Recherche.js   # Page de recherche de livres
│   │   ├── Gestion.js     # Page de gestion des livres
│   │   └── Dashboard.js   # Tableau de bord (bibliothécaires)
│   ├── services/          # Services API (appels backend)
│   ├── utils/             # Utilitaires (authentification, validation)
│   ├── App.js             # Composant principal
│   ├── App.css            # Styles de l'application
│   ├── index.js           # Point d'entrée React
│   └── index.css          # Styles globaux
├── package.json           # Dépendances et scripts npm
└── README.md              # Ce fichier
```

## Installation

1. Installer les dépendances :
```bash
npm install
```

2. Lancer l'application en mode développement :
```bash
npm start
```

L'application sera accessible sur `http://localhost:3000`

## Fonctionnalités à développer

- Page de recherche de livres
- Page de gestion des livres (CRUD)
- Gestion des emprunts et retours
- Authentification et gestion des utilisateurs
- Tableau de bord avec statistiques (réservé aux bibliothécaires)
- Interface responsive (web et mobile)

