# Backend - Application de Gestion de Bibliothèque

## Description

Backend développé en Python pour la gestion de la bibliothèque universitaire.

## Structure du projet

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée principal
│   ├── models/              # Modèles de données (livres, utilisateurs, emprunts)
│   ├── routes/              # Routes API
│   ├── services/            # Services métier
│   └── utils/               # Utilitaires (authentification, validation, etc.)
├── tests/                   # Tests unitaires
├── requirements.txt         # Dépendances Python
└── README.md               # Ce fichier
```

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Base de données

Le projet utilise MySQL comme base de données relationnelle.

## Fonctionnalités à développer

- Gestion des livres (CRUD)
- Gestion des emprunts et retours
- Authentification et gestion des utilisateurs (bibliothécaire, étudiant, enseignant)
- Tableau de bord avec statistiques (réservé aux bibliothécaires)
- Notifications et rappels (J-30 et J-5)

