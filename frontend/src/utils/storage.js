// Utilitaires pour le localStorage

// Sauvegarder une valeur dans le localStorage
export const setItem = (key, value) => {
  try {
    const serializedValue = JSON.stringify(value);
    localStorage.setItem(key, serializedValue);
    return true;
  } catch (error) {
    console.error('Erreur lors de la sauvegarde dans le localStorage:', error);
    return false;
  }
};

// Récupérer une valeur du localStorage
export const getItem = (key, defaultValue = null) => {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error('Erreur lors de la récupération depuis le localStorage:', error);
    return defaultValue;
  }
};

// Supprimer une valeur du localStorage
export const removeItem = (key) => {
  try {
    localStorage.removeItem(key);
    return true;
  } catch (error) {
    console.error('Erreur lors de la suppression depuis le localStorage:', error);
    return false;
  }
};

// Vider tout le localStorage
export const clear = () => {
  try {
    localStorage.clear();
    return true;
  } catch (error) {
    console.error('Erreur lors du nettoyage du localStorage:', error);
    return false;
  }
};

// Vérifier si une clé existe
export const hasItem = (key) => {
  return localStorage.getItem(key) !== null;
};

// Gestion du token d'authentification
export const auth = {
  saveToken: (token) => setItem('token', token),
  getToken: () => getItem('token'),
  removeToken: () => removeItem('token'),
  hasToken: () => hasItem('token'),
};

// Gestion des informations utilisateur
export const user = {
  saveUser: (userData) => setItem('user', userData),
  getUser: () => getItem('user'),
  removeUser: () => removeItem('user'),
  hasUser: () => hasItem('user'),
};

export default {
  setItem,
  getItem,
  removeItem,
  clear,
  hasItem,
  auth,
  user
};

