import api from './api';

export const authService = {
  // Connexion
  login: async (email, password) => {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erreur de connexion');
    }

    const data = await response.json();
    
    // Stocker le token et les informations utilisateur
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  },

  // Inscription
  register: async (userData) => {
    const response = await fetch('http://localhost:5000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erreur lors de l\'inscription');
    }

    return response.json();
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

