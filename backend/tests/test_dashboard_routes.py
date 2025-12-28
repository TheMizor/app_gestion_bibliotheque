"""
Tests unitaires pour les routes du tableau de bord
"""
import pytest
from unittest.mock import patch, MagicMock
from app.models.utilisateur import Role


class TestDashboardRoutes:
    """Tests pour les routes du tableau de bord"""
    
    def test_get_stats_success(self, client, auth_headers_bibliothecaire):
        """Test de récupération des statistiques (bibliothécaire)"""
        with patch('app.routes.dashboard_routes.LivreService') as mock_livre_service, \
             patch('app.routes.dashboard_routes.UtilisateurService') as mock_user_service, \
             patch('app.routes.dashboard_routes.EmpruntService') as mock_emprunt_service:
            
            mock_livre_instance = MagicMock()
            mock_livre_service.return_value = mock_livre_instance
            mock_livre_instance.get_all.return_value = {'total': 100}
            
            mock_user_instance = MagicMock()
            mock_user_service.return_value = mock_user_instance
            mock_user_instance.get_all.return_value = {'total': 50, 'utilisateurs': []}
            
            mock_emprunt_instance = MagicMock()
            mock_emprunt_service.return_value = mock_emprunt_instance
            mock_emprunt_instance.get_all.return_value = {'total': 30}
            mock_emprunt_instance.get_emprunts_en_retard.return_value = []
            
            response = client.get('/api/dashboard/stats', headers=auth_headers_bibliothecaire)
            assert response.status_code == 200
            data = response.get_json()
            assert 'total_books' in data
            assert 'total_users' in data
            assert 'active_loans' in data
    
    def test_get_stats_forbidden(self, client, auth_headers_etudiant):
        """Test de récupération des statistiques par un non-bibliothécaire"""
        response = client.get('/api/dashboard/stats', headers=auth_headers_etudiant)
        assert response.status_code == 403
    
    def test_get_notifications_success(self, client, auth_headers_bibliothecaire):
        """Test de récupération des notifications (bibliothécaire)"""
        with patch('app.routes.dashboard_routes.EmpruntService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            mock_emprunt = MagicMock()
            mock_emprunt.id = 1
            mock_emprunt.date_retour_prevue = '2025-12-31'
            mock_emprunt.livre_titre = 'Test Book'
            mock_emprunt.utilisateur_nom = 'Test User'
            mock_emprunt.utilisateur_email = 'test@test.com'
            
            mock_instance.get_rappels_30_jours.return_value = [mock_emprunt]
            mock_instance.get_rappels_5_jours.return_value = []
            
            response = client.get('/api/dashboard/notifications', headers=auth_headers_bibliothecaire)
            assert response.status_code == 200
            data = response.get_json()
            assert 'notifications' in data
    
    def test_get_notifications_forbidden(self, client, auth_headers_etudiant):
        """Test de récupération des notifications par un non-bibliothécaire"""
        response = client.get('/api/dashboard/notifications', headers=auth_headers_etudiant)
        assert response.status_code == 403

