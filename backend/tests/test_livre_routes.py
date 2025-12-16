"""
Tests unitaires pour les routes de gestion des livres
"""
import pytest
from unittest.mock import patch, MagicMock
from app.models.utilisateur import Role


class TestLivreRoutes:
    """Tests pour les routes de gestion des livres"""
    
    def test_get_livres_success(self, client, auth_headers_etudiant):
        """Test de récupération de la liste des livres"""
        with patch('app.routes.livre_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_livre = MagicMock()
            mock_livre.to_dict.return_value = {
                'id': 1,
                'titre': 'Test Book',
                'auteur': 'Test Author',
                'isbn': '1234567890',
                'disponible': True
            }
            
            mock_instance.get_all.return_value = {
                'livres': [mock_livre],
                'total': 1,
                'page': 1,
                'limit': 20
            }
            
            response = client.get('/api/books', headers=auth_headers_etudiant)
            assert response.status_code == 200
            data = response.get_json()
            assert 'books' in data
            assert len(data['books']) == 1
    
    def test_get_livres_unauthorized(self, client):
        """Test de récupération sans authentification"""
        response = client.get('/api/books')
        assert response.status_code == 401
    
    def test_get_livre_by_id_success(self, client, auth_headers_etudiant):
        """Test de récupération d'un livre par ID"""
        with patch('app.routes.livre_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_livre = MagicMock()
            mock_livre.to_dict.return_value = {
                'id': 1,
                'titre': 'Test Book',
                'auteur': 'Test Author'
            }
            
            mock_instance.get_by_id.return_value = mock_livre
            
            response = client.get('/api/books/1', headers=auth_headers_etudiant)
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == 1
    
    def test_get_livre_not_found(self, client, auth_headers_etudiant):
        """Test de récupération d'un livre inexistant"""
        with patch('app.routes.livre_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            mock_instance.get_by_id.return_value = None
            
            response = client.get('/api/books/999', headers=auth_headers_etudiant)
            assert response.status_code == 404
    
    def test_create_livre_success(self, client, auth_headers_bibliothecaire):
        """Test de création d'un livre (bibliothécaire)"""
        with patch('app.routes.livre_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_livre = MagicMock()
            mock_livre.to_dict.return_value = {
                'id': 1,
                'titre': 'New Book',
                'auteur': 'New Author'
            }
            
            mock_instance.create.return_value = mock_livre
            
            response = client.post('/api/books', 
                                  json={'titre': 'New Book', 'auteur': 'New Author'},
                                  headers=auth_headers_bibliothecaire)
            assert response.status_code == 201
    
    def test_create_livre_forbidden(self, client, auth_headers_etudiant):
        """Test de création d'un livre par un non-bibliothécaire"""
        response = client.post('/api/books',
                              json={'titre': 'New Book', 'auteur': 'New Author'},
                              headers=auth_headers_etudiant)
        assert response.status_code == 403
    
    def test_update_livre_success(self, client, auth_headers_bibliothecaire):
        """Test de mise à jour d'un livre (bibliothécaire)"""
        with patch('app.routes.livre_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_livre = MagicMock()
            mock_livre.to_dict.return_value = {
                'id': 1,
                'titre': 'Updated Book',
                'auteur': 'Updated Author'
            }
            
            mock_instance.update.return_value = mock_livre
            
            response = client.put('/api/books/1',
                                json={'titre': 'Updated Book'},
                                headers=auth_headers_bibliothecaire)
            assert response.status_code == 200
    
    def test_delete_livre_success(self, client, auth_headers_bibliothecaire):
        """Test de suppression d'un livre (bibliothécaire)"""
        with patch('app.routes.livre_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            mock_instance.delete.return_value = True
            
            response = client.delete('/api/books/1', headers=auth_headers_bibliothecaire)
            assert response.status_code == 200
    
    def test_delete_livre_not_found(self, client, auth_headers_bibliothecaire):
        """Test de suppression d'un livre inexistant"""
        with patch('app.routes.livre_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            mock_instance.delete.return_value = False
            
            response = client.delete('/api/books/999', headers=auth_headers_bibliothecaire)
            assert response.status_code == 404

