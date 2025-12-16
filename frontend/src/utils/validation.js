// Validation des emails
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validation des mots de passe
export const isValidPassword = (password) => {
  // Au moins 6 caractères
  return password && password.length >= 6;
};

// Validation des ISBN (10 ou 13 chiffres)
export const isValidISBN = (isbn) => {
  const isbnRegex = /^(?:\d{10}|\d{13})$/;
  return isbnRegex.test(isbn.replace(/-/g, ''));
};

// Validation d'une année
export const isValidYear = (year) => {
  const currentYear = new Date().getFullYear();
  const yearNum = parseInt(year, 10);
  return yearNum >= 1000 && yearNum <= currentYear;
};

// Validation d'un champ requis
export const isRequired = (value) => {
  return value !== null && value !== undefined && value.toString().trim() !== '';
};

// Validation d'un livre complet
export const validateLivre = (livre) => {
  const errors = {};

  if (!isRequired(livre.titre)) {
    errors.titre = 'Le titre est requis';
  }

  if (!isRequired(livre.auteur)) {
    errors.auteur = 'L\'auteur est requis';
  }

  if (!isRequired(livre.isbn)) {
    errors.isbn = 'L\'ISBN est requis';
  } else if (!isValidISBN(livre.isbn)) {
    errors.isbn = 'L\'ISBN doit contenir 10 ou 13 chiffres';
  }

  if (!isRequired(livre.annee_publication)) {
    errors.annee_publication = 'L\'année de publication est requise';
  } else if (!isValidYear(livre.annee_publication)) {
    errors.annee_publication = 'L\'année de publication est invalide';
  }

  if (!isRequired(livre.categorie)) {
    errors.categorie = 'La catégorie est requise';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

// Validation d'un utilisateur
export const validateUser = (user) => {
  const errors = {};

  if (!isRequired(user.nom)) {
    errors.nom = 'Le nom est requis';
  }

  if (!isRequired(user.prenom)) {
    errors.prenom = 'Le prénom est requis';
  }

  if (!isRequired(user.email)) {
    errors.email = 'L\'email est requis';
  } else if (!isValidEmail(user.email)) {
    errors.email = 'L\'email est invalide';
  }

  if (!isRequired(user.password)) {
    errors.password = 'Le mot de passe est requis';
  } else if (!isValidPassword(user.password)) {
    errors.password = 'Le mot de passe doit contenir au moins 6 caractères';
  }

  if (!isRequired(user.role)) {
    errors.role = 'Le rôle est requis';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

export default {
  isValidEmail,
  isValidPassword,
  isValidISBN,
  isValidYear,
  isRequired,
  validateLivre,
  validateUser
};

