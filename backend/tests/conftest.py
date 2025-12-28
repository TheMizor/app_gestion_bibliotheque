"""
Configuration et fixtures pour les tests
"""
import pytest
import os
os.environ['TESTING'] = 'True'

from app.main import app
from app.utils.auth import generate_token
from app.models.utilisateur import Role
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_auth_user_service():
    """Mock automatique du service utilisateur pour l'authentification"""
    with patch('app.utils.auth.UtilisateurService') as mock_service_cls:
        mock_service = mock_service_cls.return_value
        
        def get_by_id_side_effect(user_id):
            print(f"DEBUG: Mock User Service get_by_id called with {user_id}")
            user = MagicMock()
            user.id = user_id
            if user_id == 1:
                user.role = Role.BIBLIOTHECAIRE
                user.is_bibliothecaire.return_value = True
                print(f"DEBUG: Returning BIBLIOTHECAIRE user")
            elif user_id == 2:
                user.role = Role.ETUDIANT
                user.is_bibliothecaire.return_value = False
                print(f"DEBUG: Returning ETUDIANT user")
            elif user_id == 3:
                user.role = Role.ENSEIGNANT
                user.is_bibliothecaire.return_value = False
            else:
                return None
            
            user.to_dict.return_value = {
                'id': user_id,
                'nom': f'User {user_id}',
                'email': f'user{user_id}@test.com',
                'role': user.role if user and hasattr(user, 'role') else 'etudiant'
            }
            return user
            
        mock_service.get_by_id.side_effect = get_by_id_side_effect
        yield mock_service


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token_bibliothecaire():
    """Fixture pour générer un token JWT de bibliothécaire"""
    return generate_token(1, Role.BIBLIOTHECAIRE)


@pytest.fixture
def auth_token_etudiant():
    """Fixture pour générer un token JWT d'étudiant"""
    return generate_token(2, Role.ETUDIANT)


@pytest.fixture
def auth_token_enseignant():
    """Fixture pour générer un token JWT d'enseignant"""
    return generate_token(3, Role.ENSEIGNANT)


@pytest.fixture
def auth_headers_bibliothecaire(auth_token_bibliothecaire):
    """Headers d'authentification pour bibliothécaire"""
    return {'Authorization': f'Bearer {auth_token_bibliothecaire}'}


@pytest.fixture
def auth_headers_etudiant(auth_token_etudiant):
    """Headers d'authentification pour étudiant"""
    return {'Authorization': f'Bearer {auth_token_etudiant}'}


@pytest.fixture
def auth_headers_enseignant(auth_token_enseignant):
    """Headers d'authentification pour enseignant"""
    return {'Authorization': f'Bearer {auth_token_enseignant}'}

