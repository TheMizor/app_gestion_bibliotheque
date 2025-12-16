# Tests Unitaires

## Description

Tests unitaires pour l'application backend de gestion de bibliothèque.

## Structure

- `conftest.py` - Configuration pytest et fixtures partagées
- `test_auth_routes.py` - Tests pour les routes d'authentification
- `test_livre_routes.py` - Tests pour les routes de gestion des livres
- `test_utilisateur_routes.py` - Tests pour les routes de gestion des utilisateurs
- `test_emprunt_routes.py` - Tests pour les routes de gestion des emprunts
- `test_dashboard_routes.py` - Tests pour les routes du tableau de bord

## Installation

Les dépendances de test sont déjà incluses dans `requirements.txt` :
- `pytest==7.4.3`
- `pytest-cov==4.1.0`

## Exécution des tests

### Tous les tests

```bash
cd backend
pytest
```

### Tests avec couverture de code

```bash
pytest --cov=app --cov-report=html
```

### Tests spécifiques

```bash
# Tester un fichier spécifique
pytest tests/test_auth_routes.py

# Tester une classe spécifique
pytest tests/test_auth_routes.py::TestAuthRoutes

# Tester une fonction spécifique
pytest tests/test_auth_routes.py::TestAuthRoutes::test_login_success
```

### Mode verbeux

```bash
pytest -v
```

## Fixtures disponibles

- `client` - Client Flask de test
- `auth_token_bibliothecaire` - Token JWT pour bibliothécaire
- `auth_token_etudiant` - Token JWT pour étudiant
- `auth_token_enseignant` - Token JWT pour enseignant
- `auth_headers_bibliothecaire` - Headers d'authentification pour bibliothécaire
- `auth_headers_etudiant` - Headers d'authentification pour étudiant
- `auth_headers_enseignant` - Headers d'authentification pour enseignant

## Notes

Les tests utilisent des mocks pour éviter les dépendances à la base de données réelle. Tous les services sont mockés pour isoler les tests des routes.

