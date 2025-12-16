// Fonctions utilitaires diverses

// Capitaliser la première lettre d'une chaîne
export const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

// Tronquer un texte à une longueur donnée
export const truncate = (str, maxLength = 50) => {
  if (!str || str.length <= maxLength) return str;
  return str.substring(0, maxLength) + '...';
};

// Formater un nombre avec des espaces pour les milliers
export const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
};

// Générer un ID aléatoire
export const generateId = () => {
  return '_' + Math.random().toString(36).substr(2, 9);
};

// Débounce une fonction
export const debounce = (func, delay = 300) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

// Filtrer un tableau d'objets par propriété
export const filterByProperty = (array, property, value) => {
  return array.filter(item => 
    item[property].toString().toLowerCase().includes(value.toLowerCase())
  );
};

// Trier un tableau d'objets par propriété
export const sortByProperty = (array, property, ascending = true) => {
  return [...array].sort((a, b) => {
    const aVal = a[property];
    const bVal = b[property];
    
    if (aVal < bVal) return ascending ? -1 : 1;
    if (aVal > bVal) return ascending ? 1 : -1;
    return 0;
  });
};

// Grouper un tableau d'objets par propriété
export const groupBy = (array, property) => {
  return array.reduce((acc, item) => {
    const key = item[property];
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(item);
    return acc;
  }, {});
};

// Vérifier si un objet est vide
export const isEmpty = (obj) => {
  return Object.keys(obj).length === 0;
};

// Copier dans le presse-papiers
export const copyToClipboard = (text) => {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text);
  } else {
    // Fallback pour les navigateurs plus anciens
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    return Promise.resolve();
  }
};

// Télécharger un fichier
export const downloadFile = (data, filename, type = 'text/plain') => {
  const blob = new Blob([data], { type });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

export default {
  capitalize,
  truncate,
  formatNumber,
  generateId,
  debounce,
  filterByProperty,
  sortByProperty,
  groupBy,
  isEmpty,
  copyToClipboard,
  downloadFile
};

