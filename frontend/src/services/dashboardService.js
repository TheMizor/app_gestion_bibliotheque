import api from './api';

export const dashboardService = {
  // Récupérer les statistiques du tableau de bord
  getStats: async () => {
    return api.get('/dashboard/stats');
  },

  // Récupérer les emprunts récents
  getRecentEmprunts: async (limit = 10) => {
    return api.get(`/loans?limit=${limit}`);
  },

  // Récupérer les statistiques des auteurs populaires
  getTopAuthors: async (limit = 10) => {
    return api.get(`/dashboard/stats/authors?limit=${limit}`);
  },

  // Récupérer les notifications en attente
  getNotifications: async () => {
    return api.get('/dashboard/notifications');
  },
};

export default dashboardService;

