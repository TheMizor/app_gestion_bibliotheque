import api from './api';

export const livreService = {
  // Récupérer tous les livres
  getAllLivres: async () => {
    return api.get('/books');
  },

  // Récupérer un livre par son ID
  getLivreById: async (id) => {
    return api.get(`/books/${id}`);
  },

  // Rechercher des livres
  searchLivres: async (query) => {
    return api.get(`/books/search?q=${encodeURIComponent(query)}`);
  },

  // Créer un nouveau livre
  createLivre: async (livreData) => {
    return api.post('/books', livreData);
  },

  // Mettre à jour un livre
  updateLivre: async (id, livreData) => {
    return api.put(`/books/${id}`, livreData);
  },

  // Supprimer un livre
  deleteLivre: async (id) => {
    return api.delete(`/books/${id}`);
  },

  // Vérifier la disponibilité d'un livre
  checkDisponibilite: async (id) => {
    return api.get(`/books/${id}/disponibilite`);
  },
};

export default livreService;

