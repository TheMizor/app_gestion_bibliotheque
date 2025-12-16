// Formater une date en format français
export const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// Formater une date en format court
export const formatDateShort = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('fr-FR');
};

// Formater une date avec l'heure
export const formatDateTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Calculer le nombre de jours entre deux dates
export const daysBetween = (date1, date2) => {
  const d1 = new Date(date1);
  const d2 = new Date(date2);
  const diffTime = Math.abs(d2 - d1);
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

// Vérifier si une date est dans le passé
export const isPast = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  return date < now;
};

// Vérifier si une date est dans le futur
export const isFuture = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  return date > now;
};

// Ajouter des jours à une date
export const addDays = (dateString, days) => {
  const date = new Date(dateString);
  date.setDate(date.getDate() + days);
  return date.toISOString();
};

// Calculer la date de retour prévue (60 jours par défaut)
export const calculateReturnDate = (empruntDate, daysToAdd = 60) => {
  return addDays(empruntDate, daysToAdd);
};

// Vérifier si un emprunt est en retard
export const isEmpruntEnRetard = (dateRetourPrevue, dateRetourEffective = null) => {
  if (dateRetourEffective) {
    return false; // Déjà retourné
  }
  return isPast(dateRetourPrevue);
};

// Calculer le nombre de jours de retard
export const joursDeRetard = (dateRetourPrevue) => {
  if (!isPast(dateRetourPrevue)) {
    return 0;
  }
  const now = new Date();
  const dateRetour = new Date(dateRetourPrevue);
  return daysBetween(dateRetour, now);
};

export default {
  formatDate,
  formatDateShort,
  formatDateTime,
  daysBetween,
  isPast,
  isFuture,
  addDays,
  calculateReturnDate,
  isEmpruntEnRetard,
  joursDeRetard
};

