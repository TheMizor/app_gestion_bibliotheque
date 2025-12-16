// Constantes de l'application

// Rôles utilisateur
export const ROLES = {
  ETUDIANT: 'etudiant',
  ENSEIGNANT: 'enseignant',
  BIBLIOTHECAIRE: 'bibliothecaire'
};

// Durées d'emprunt (en jours)
export const DUREE_EMPRUNT = {
  ETUDIANT: 30,
  ENSEIGNANT: 60,
  DEFAUT: 30
};

// Délais de notification (en jours avant la date de retour)
export const NOTIFICATION_DELAIS = {
  PREMIERE_NOTIFICATION: 30,
  RAPPEL: 5
};

// Statuts d'emprunt
export const STATUT_EMPRUNT = {
  EN_COURS: 'en_cours',
  RETOURNE: 'retourne',
  RETARD: 'retard'
};

// Messages d'erreur
export const ERROR_MESSAGES = {
  CONNEXION_FAILED: 'Erreur de connexion au serveur',
  AUTH_FAILED: 'Email ou mot de passe incorrect',
  SESSION_EXPIRED: 'Votre session a expiré, veuillez vous reconnecter',
  UNAUTHORIZED: 'Vous n\'avez pas les droits nécessaires',
  NOT_FOUND: 'Ressource non trouvée',
  LIVRE_INDISPONIBLE: 'Ce livre n\'est pas disponible',
  VALIDATION_ERROR: 'Veuillez vérifier les informations saisies'
};

// Messages de succès
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Connexion réussie',
  REGISTER_SUCCESS: 'Inscription réussie',
  LIVRE_CREATED: 'Livre ajouté avec succès',
  LIVRE_UPDATED: 'Livre modifié avec succès',
  LIVRE_DELETED: 'Livre supprimé avec succès',
  EMPRUNT_CREATED: 'Emprunt enregistré avec succès',
  RETOUR_REGISTERED: 'Retour enregistré avec succès'
};

// Catégories de livres
export const CATEGORIES = [
  'Roman',
  'Science-Fiction',
  'Fantastique',
  'Policier',
  'Thriller',
  'Histoire',
  'Biographie',
  'Sciences',
  'Informatique',
  'Mathématiques',
  'Philosophie',
  'Psychologie',
  'Art',
  'Littérature',
  'Jeunesse',
  'Bande Dessinée',
  'Autre'
];

// Configuration de pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [5, 10, 20, 50]
};

// URLs
// Utiliser le proxy relatif - setupProxy.js intercepte /api/* et redirige vers le backend
export const API_BASE_URL = '/api';

export default {
  ROLES,
  DUREE_EMPRUNT,
  NOTIFICATION_DELAIS,
  STATUT_EMPRUNT,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  CATEGORIES,
  PAGINATION,
  API_BASE_URL
};

