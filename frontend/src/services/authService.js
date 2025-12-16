import api from './api';

export const authService = {
  // Connexion
  login: async (email, password) => {
    // Utilisation directe de fetch pour login car pas besoin de token auth
    const response = await api.post('/auth/login', { email, password });
    
    // Stocker le token et les informations utilisateur
    localStorage.setItem('token', response.token);
    localStorage.setItem('user', JSON.stringify(response.user));
    
    return response;
  },

  // Inscription
  register: async (userData) => {
    return api.post('/auth/register', userData);
  },

  // Déconnexion
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  // Vérifier si l'utilisateur est connecté
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },

  // Récupérer l'utilisateur courant
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Vérifier le rôle de l'utilisateur
  hasRole: (role) => {
    const user = authService.getCurrentUser();
    return user && user.role === role;
  },

  // Vérifier si l'utilisateur est bibliothécaire
  isBibliothecaire: () => {
    return authService.hasRole('bibliothecaire');
  },
};

export default authService;

