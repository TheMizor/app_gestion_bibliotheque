"""
Tests unitaires pour les routes de gestion des emprunts
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.models.utilisateur import Role
from app.models.emprunt import StatutEmprunt


class TestEmpruntRoutes:
    """Tests pour les routes de gestion des emprunts"""
    
    def test_get_emprunts_success(self, client, auth_headers_etudiant):
        """Test de récupération de la liste des emprunts"""
        with patch('app.routes.emprunt_routes.EmpruntService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_emprunt = MagicMock()
            mock_emprunt.to_dict.return_value = {
                'id': 1,
                'livre_id': 1,
                'utilisateur_id': 2,
                'statut': StatutEmprunt.ACTIF
            }
            mock_emprunt.livre_titre = 'Test Book'
            mock_emprunt.livre_auteur = 'Test Author'
            mock_emprunt.utilisateur_nom = 'Test User'
            mock_emprunt.utilisateur_email = 'test@example.com'
            
            mock_instance.get_all.return_value = {
                'emprunts': [mock_emprunt],
                'total': 1,
                'page': 1,
                'limit': 20
            }
            
            response = client.get('/api/loans', headers=auth_headers_etudiant)
            assert response.status_code == 200
            data = response.get_json()
            assert 'loans' in data
    
    def test_get_emprunt_by_id_success(self, client, auth_headers_etudiant):
        """Test de récupération d'un emprunt par ID"""
        with patch('app.routes.emprunt_routes.EmpruntService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_emprunt = MagicMock()
            mock_emprunt.utilisateur_id = 2
            mock_emprunt.to_dict.return_value = {
                'id': 1,
                'livre_id': 1,
                'utilisateur_id': 2,
                'statut': StatutEmprunt.ACTIF
            }
            mock_emprunt.livre_titre = 'Test Book'
            mock_emprunt.livre_auteur = 'Test Author'
            mock_emprunt.utilisateur_nom = 'Test User'
            mock_emprunt.utilisateur_email = 'test@example.com'
            
            mock_instance.get_by_id.return_value = mock_emprunt
            
            response = client.get('/api/loans/1', headers=auth_headers_etudiant)
            assert response.status_code == 200
    
    def test_create_emprunt_success(self, client, auth_headers_etudiant):
        """Test de création d'un emprunt"""
        with patch('app.routes.emprunt_routes.EmpruntService') as mock_emprunt_service, \
             patch('app.routes.emprunt_routes.LivreService') as mock_livre_service:
            
            mock_emprunt_instance = MagicMock()
            mock_emprunt_service.return_value = mock_emprunt_instance
            
            mock_livre_instance = MagicMock()
            mock_livre_service.return_value = mock_livre_instance
            
            mock_livre = MagicMock()
            mock_livre.exemplaires_disponibles = 5
            mock_livre_instance.get_by_id.return_value = mock_livre
            
            mock_emprunt = MagicMock()
            mock_emprunt.to_dict.return_value = {
                'id': 1,
                'livre_id': 1,
                'utilisateur_id': 2,
                'statut': StatutEmprunt.ACTIF
            }
            mock_emprunt.livre_titre = 'Test Book'
            mock_emprunt.livre_auteur = 'Test Author'
            mock_emprunt.utilisateur_nom = 'Test User'
            mock_emprunt.utilisateur_email = 'test@example.com'
            
            mock_emprunt_instance.create.return_value = mock_emprunt
            
            response = client.post('/api/loans',
                                  json={'book_id': 1},
                                  headers=auth_headers_etudiant)
            assert response.status_code == 201
    
    def test_create_emprunt_book_not_available(self, client, auth_headers_etudiant):
        """Test de création d'un emprunt pour un livre non disponible"""
        with patch('app.routes.emprunt_routes.LivreService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_livre = MagicMock()
            mock_livre.exemplaires_disponibles = 0
            mock_instance.get_by_id.return_value = mock_livre
            
            response = client.post('/api/loans',
                                  json={'book_id': 1},
                                  headers=auth_headers_etudiant)
            assert response.status_code == 400
    
    def test_retourner_livre_success(self, client, auth_headers_etudiant):
        """Test de retour d'un livre"""
        with patch('app.routes.emprunt_routes.EmpruntService') as mock_emprunt_service, \
             patch('app.routes.emprunt_routes.LivreService') as mock_livre_service:
            
            mock_emprunt_instance = MagicMock()
            mock_emprunt_service.return_value = mock_emprunt_instance
            
            mock_livre_instance = MagicMock()
            mock_livre_service.return_value = mock_livre_instance
            
            mock_emprunt = MagicMock()
            mock_emprunt.utilisateur_id = 2
            mock_emprunt.livre_id = 1
            mock_emprunt.statut = StatutEmprunt.ACTIF
            mock_emprunt.to_dict.return_value = {
                'id': 1,
                'statut': StatutEmprunt.RETOURNE
            }
            mock_emprunt.livre_titre = 'Test Book'
            mock_emprunt.livre_auteur = 'Test Author'
            mock_emprunt.utilisateur_nom = 'Test User'
            mock_emprunt.utilisateur_email = 'test@example.com'
            
            mock_emprunt_instance.get_by_id.return_value = mock_emprunt
            mock_emprunt_instance.retourner.return_value = mock_emprunt
            
            response = client.put('/api/loans/1/return', headers=auth_headers_etudiant)
            assert response.status_code == 200
    
    def test_retourner_livre_already_returned(self, client, auth_headers_etudiant):
        """Test de retour d'un livre déjà retourné"""
        with patch('app.routes.emprunt_routes.EmpruntService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_emprunt = MagicMock()
            mock_emprunt.utilisateur_id = 2
            mock_emprunt.statut = StatutEmprunt.RETOURNE
            
            mock_instance.get_by_id.return_value = mock_emprunt
            
            response = client.put('/api/loans/1/return', headers=auth_headers_etudiant)
            assert response.status_code == 400

