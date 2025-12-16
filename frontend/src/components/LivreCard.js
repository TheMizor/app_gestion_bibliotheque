import React from 'react';
import '../App.css';

function LivreCard({ livre, onEmprunt, showEmpruntButton = true }) {
  return (
    <div className="livre-card">
      <div className="livre-header">
        <h3>{livre.titre}</h3>
        <span className={livre.disponible ? 'badge-disponible' : 'badge-indisponible'}>
          {livre.disponible ? '✓ Disponible' : '✗ Emprunté'}
        </span>
      </div>
      
      <div className="livre-details">
        <p><strong>Auteur:</strong> {livre.auteur}</p>
        <p><strong>ISBN:</strong> {livre.isbn}</p>
        <p><strong>Année:</strong> {livre.annee_publication}</p>
        <p><strong>Catégorie:</strong> {livre.categorie}</p>
      </div>
      
      {showEmpruntButton && livre.disponible && (
        <button 
          onClick={() => onEmprunt(livre.id)}
          className="btn-emprunt"
        >
          Emprunter
        </button>
      )}
    </div>
  );
}

export default LivreCard;

