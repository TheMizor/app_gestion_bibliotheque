"""
Tests unitaires pour les routes d'authentification
"""
import pytest
from unittest.mock import patch, MagicMock
from app.models.utilisateur import Role


class TestAuthRoutes:
    """Tests pour les routes d'authentification"""
    
    def test_health_check(self, client):
        """Test de l'endpoint health check"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
    
    def test_login_success(self, client):
        """Test de connexion réussie"""
        with patch('app.routes.auth_routes.UtilisateurService') as MockService:
            mock_instance = MagicMock()
            MockService.return_value = mock_instance
            
            # Mock utilisateur
            mock_user = MagicMock()
            mock_user.id = 1
            mock_user.role = Role.ETUDIANT
            mock_user.to_dict.return_value = {'id': 1, 'nom': 'Test', 'email': 'test@test.com', 'role': 'etudiant'}
            
            mock_instance.get_by_email.return_value = mock_user
            mock_instance.verify_password.return_value = True
            
            response = client.post('/api/auth/login', json={
                'email': 'test@test.com',
                'password': 'password123'
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'token' in data
            assert 'user' in data
    
    def test_login_invalid_credentials(self, client):
        """Test de connexion avec identifiants invalides"""
        with patch('app.routes.auth_routes.UtilisateurService') as MockService:
            mock_instance = MagicMock()
            MockService.return_value = mock_instance
            mock_instance.get_by_email.return_value = None
            
            response = client.post('/api/auth/login', json={
                'email': 'test@test.com',
                'password': 'wrongpassword'
            })
            
            assert response.status_code == 401
    
    def test_login_missing_fields(self, client):
        """Test de connexion avec champs manquants"""
        response = client.post('/api/auth/login', json={})
        assert response.status_code == 400
    
    def test_get_current_user(self, client, auth_headers_etudiant):
        """Test de récupération de l'utilisateur connecté"""
        with patch('app.routes.auth_routes.get_current_user') as mock_get_user:
            mock_user = MagicMock()
            mock_user.id = 2
            mock_user.role = Role.ETUDIANT
            mock_user.to_dict.return_value = {'id': 2, 'nom': 'Test', 'email': 'test@test.com', 'role': 'etudiant'}
            mock_get_user.return_value = mock_user
            
            response = client.get('/api/auth/me', headers=auth_headers_etudiant)
            assert response.status_code == 200
    
    def test_get_current_user_unauthorized(self, client):
        """Test de récupération sans authentification"""
        response = client.get('/api/auth/me')
        assert response.status_code == 401
    
    def test_register_success(self, client):
        """Test d'inscription réussie"""
        with patch('app.routes.auth_routes.UtilisateurService') as MockService, \
             patch('app.routes.auth_routes.get_current_user') as mock_get_user:
            mock_get_user.return_value = None  # Pas d'utilisateur connecté
            
            mock_instance = MagicMock()
            MockService.return_value = mock_instance
            
            mock_user = MagicMock()
            mock_user.id = 1
            mock_user.role = Role.ETUDIANT
            mock_user.to_dict.return_value = {'id': 1, 'nom': 'New User', 'email': 'new@test.com', 'role': 'etudiant'}
            
            mock_instance.create.return_value = mock_user
            
            response = client.post('/api/auth/register', json={
                'nom': 'New User',
                'email': 'new@test.com',
                'password': 'password123'
            })
            
            assert response.status_code == 201
            data = response.get_json()
            assert 'token' in data
            assert 'user' in data
    
    def test_register_duplicate_email(self, client):
        """Test d'inscription avec email déjà utilisé"""
        with patch('app.routes.auth_routes.UtilisateurService') as MockService, \
             patch('app.routes.auth_routes.get_current_user') as mock_get_user:
            mock_get_user.return_value = None
            
            mock_instance = MagicMock()
            MockService.return_value = mock_instance
            mock_instance.create.return_value = None
            
            response = client.post('/api/auth/register', json={
                'nom': 'New User',
                'email': 'existing@test.com',
                'password': 'password123'
            })
            
            assert response.status_code == 400

