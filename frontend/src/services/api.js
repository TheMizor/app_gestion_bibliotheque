// Configuration de base pour l'API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Fonction utilitaire pour gérer les requêtes
const fetchWithAuth = async (url, options = {}) => {
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Token expiré ou invalide
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
    throw new Error('Session expirée');
  }

  return response;
};

export const api = {
  // Méthode GET
  get: async (url) => {
    const response = await fetchWithAuth(url);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erreur lors de la requête');
    }
    return response.json();
  },

  // Méthode POST
  post: async (url, data) => {
    const response = await fetchWithAuth(url, {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erreur lors de la requête');
    }
    return response.json();
  },

  // Méthode PUT
  put: async (url, data) => {
    const response = await fetchWithAuth(url, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erreur lors de la requête');
    }
    return response.json();
  },

  // Méthode DELETE
  delete: async (url) => {
    const response = await fetchWithAuth(url, {
      method: 'DELETE',
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erreur lors de la requête');
    }
    return response.json();
  },
};

export default api;

