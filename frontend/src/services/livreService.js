import api from './api';

export const livreService = {
  // Récupérer tous les livres
  getAllLivres: async () => {
    return api.get('/livres');
  },

  // Récupérer un livre par son ID
  getLivreById: async (id) => {
    return api.get(`/livres/${id}`);
  },

  // Rechercher des livres
  searchLivres: async (query) => {
    return api.get(`/livres/search?q=${encodeURIComponent(query)}`);
  },

  // Créer un nouveau livre
  createLivre: async (livreData) => {
    return api.post('/livres', livreData);
  },

  // Mettre à jour un livre
  updateLivre: async (id, livreData) => {
    return api.put(`/livres/${id}`, livreData);
  },

  // Supprimer un livre
  deleteLivre: async (id) => {
    return api.delete(`/livres/${id}`);
  },

  // Vérifier la disponibilité d'un livre
  checkDisponibilite: async (id) => {
    return api.get(`/livres/${id}/disponibilite`);
  },
};

export default livreService;

