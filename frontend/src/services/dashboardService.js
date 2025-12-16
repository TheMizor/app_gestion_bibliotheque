import api from './api';

export const dashboardService = {
  // Récupérer les statistiques du tableau de bord
  getStats: async () => {
    return api.get('/dashboard/stats');
  },

  // Récupérer les emprunts récents
  getRecentEmprunts: async (limit = 10) => {
    return api.get(`/emprunts?limit=${limit}`);
  },

  // Récupérer les livres les plus empruntés
  getTopLivres: async (limit = 5) => {
    return api.get(`/dashboard/top-livres?limit=${limit}`);
  },

  // Récupérer les utilisateurs les plus actifs
  getTopUtilisateurs: async (limit = 5) => {
    return api.get(`/dashboard/top-utilisateurs?limit=${limit}`);
  },

  // Récupérer les notifications en attente
  getNotifications: async () => {
    return api.get('/notifications');
  },
};

export default dashboardService;

