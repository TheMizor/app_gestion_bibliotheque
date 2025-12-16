import api from './api';

export const empruntService = {
  // Récupérer tous les emprunts
  getAllEmprunts: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return api.get(`/loans${queryString ? '?' + queryString : ''}`);
  },

  // Récupérer les emprunts d'un utilisateur
  getEmpruntsByUser: async (userId) => {
    return api.get(`/loans`);
  },

  // Récupérer un emprunt par son ID
  getEmpruntById: async (id) => {
    return api.get(`/loans/${id}`);
  },

  // Créer un nouvel emprunt
  createEmprunt: async (empruntData) => {
    return api.post('/loans', empruntData);
  },

  // Enregistrer le retour d'un livre
  returnLivre: async (empruntId) => {
    return api.put(`/loans/${empruntId}/return`);
  },

  // Prolonger un emprunt
  prolongerEmprunt: async (empruntId, jours) => {
    return api.put(`/loans/${empruntId}/extend`, { jours });
  },

  // Récupérer les emprunts en retard
  getEmpruntsEnRetard: async () => {
    return api.get('/loans?status=overdue');
  },
};

export default empruntService;

