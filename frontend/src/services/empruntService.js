import api from './api';

export const empruntService = {
  // Récupérer tous les emprunts
  getAllEmprunts: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return api.get(`/emprunts${queryString ? '?' + queryString : ''}`);
  },

  // Récupérer les emprunts d'un utilisateur
  getEmpruntsByUser: async (userId) => {
    return api.get(`/emprunts/utilisateur/${userId}`);
  },

  // Récupérer un emprunt par son ID
  getEmpruntById: async (id) => {
    return api.get(`/emprunts/${id}`);
  },

  // Créer un nouvel emprunt
  createEmprunt: async (empruntData) => {
    return api.post('/emprunts', empruntData);
  },

  // Enregistrer le retour d'un livre
  returnLivre: async (empruntId) => {
    return api.put(`/emprunts/${empruntId}/retour`);
  },

  // Prolonger un emprunt
  prolongerEmprunt: async (empruntId, jours) => {
    return api.put(`/emprunts/${empruntId}/prolonger`, { jours });
  },

  // Récupérer les emprunts en retard
  getEmpruntsEnRetard: async () => {
    return api.get('/emprunts/retard');
  },
};

export default empruntService;

