"""
Configuration et fixtures pour les tests
"""
import pytest
import os
os.environ['TESTING'] = 'True'

from app.main import app
from app.utils.auth import generate_token
from app.models.utilisateur import Role


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

