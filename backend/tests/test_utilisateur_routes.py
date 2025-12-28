"""
Tests unitaires pour les routes de gestion des utilisateurs
"""
import pytest
from unittest.mock import patch, MagicMock
from app.models.utilisateur import Role


class TestUtilisateurRoutes:
    """Tests pour les routes de gestion des utilisateurs"""
    
    def test_get_utilisateurs_success(self, client, auth_headers_bibliothecaire):
        """Test de récupération de la liste des utilisateurs (bibliothécaire)"""
        with patch('app.routes.utilisateur_routes.UtilisateurService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_user = MagicMock()
            mock_user.to_dict.return_value = {
                'id': 1,
                'nom': 'Test User',
                'email': 'test@test.com',
                'role': 'etudiant'
            }
            
            mock_instance.get_all.return_value = {
                'utilisateurs': [mock_user],
                'total': 1,
                'page': 1,
                'limit': 20
            }
            
            response = client.get('/api/users', headers=auth_headers_bibliothecaire)
            assert response.status_code == 200
            data = response.get_json()
            assert 'users' in data
    
    def test_get_utilisateurs_forbidden(self, client, auth_headers_etudiant):
        """Test de récupération de la liste par un non-bibliothécaire"""
        response = client.get('/api/users', headers=auth_headers_etudiant)
        assert response.status_code == 403
    
    def test_get_utilisateur_by_id_success(self, client, auth_headers_etudiant):
        """Test de récupération d'un utilisateur par ID"""
        with patch('app.routes.utilisateur_routes.UtilisateurService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_user = MagicMock()
            mock_user.id = 2
            mock_user.to_dict.return_value = {
                'id': 2,
                'nom': 'Test User',
                'email': 'test@test.com'
            }
            
            mock_instance.get_by_id.return_value = mock_user
            
            response = client.get('/api/users/2', headers=auth_headers_etudiant)
            assert response.status_code == 200
    
    def test_get_utilisateur_not_found(self, client, auth_headers_bibliothecaire):
        """Test de récupération d'un utilisateur inexistant"""
        with patch('app.routes.utilisateur_routes.UtilisateurService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            mock_instance.get_by_id.return_value = None
            
            response = client.get('/api/users/999', headers=auth_headers_bibliothecaire)
            assert response.status_code == 404
    
    def test_create_utilisateur_success(self, client, auth_headers_bibliothecaire):
        """Test de création d'un utilisateur (bibliothécaire)"""
        with patch('app.routes.utilisateur_routes.UtilisateurService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_user = MagicMock()
            mock_user.to_dict.return_value = {
                'id': 1,
                'nom': 'New User',
                'email': 'new@test.com',
                'role': 'etudiant'
            }
            
            mock_instance.create.return_value = mock_user
            
            response = client.post('/api/users',
                                  json={
                                      'nom': 'New User',
                                      'email': 'new@test.com',
                                      'password': 'password123'
                                  },
                                  headers=auth_headers_bibliothecaire)
            assert response.status_code == 201
    
    def test_update_utilisateur_success(self, client, auth_headers_etudiant):
        """Test de mise à jour d'un utilisateur"""
        with patch('app.routes.utilisateur_routes.UtilisateurService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_user = MagicMock()
            mock_user.id = 2
            mock_user.to_dict.return_value = {
                'id': 2,
                'nom': 'Updated User',
                'email': 'test@test.com'
            }
            
            mock_instance.update.return_value = mock_user
            
            response = client.put('/api/users/2',
                                json={'nom': 'Updated User'},
                                headers=auth_headers_etudiant)
            assert response.status_code == 200
    
    def test_delete_utilisateur_success(self, client, auth_headers_bibliothecaire):
        """Test de suppression d'un utilisateur (bibliothécaire)"""
        with patch('app.routes.utilisateur_routes.UtilisateurService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            mock_instance.delete.return_value = True
            
            response = client.delete('/api/users/1', headers=auth_headers_bibliothecaire)
            assert response.status_code == 200

