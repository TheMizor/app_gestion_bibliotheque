import React, { useState, useEffect } from 'react';
import '../App.css';

function Recherche() {
  const [livres, setLivres] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredLivres, setFilteredLivres] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Charger tous les livres au démarrage
    fetchLivres();
  }, []);

  useEffect(() => {
    // Filtrer les livres en fonction du terme de recherche
    if (searchTerm.trim() === '') {
      setFilteredLivres(livres);
    } else {
      const filtered = livres.filter(livre =>
        livre.titre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        livre.auteur.toLowerCase().includes(searchTerm.toLowerCase()) ||
        livre.isbn.includes(searchTerm)
      );
      setFilteredLivres(filtered);
    }
  }, [searchTerm, livres]);

  const fetchLivres = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/livres');
      const data = await response.json();
      setLivres(data);
      setFilteredLivres(data);
    } catch (error) {
      console.error('Erreur lors du chargement des livres:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEmprunt = async (livreId) => {
    try {
      const response = await fetch('http://localhost:5000/api/emprunts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          livre_id: livreId
        })
      });

      if (response.ok) {
        alert('Emprunt enregistré avec succès !');
        fetchLivres(); // Recharger la liste
      } else {
        const error = await response.json();
        alert(`Erreur: ${error.message}`);
      }
    } catch (error) {
      console.error('Erreur lors de l\'emprunt:', error);
      alert('Erreur lors de l\'enregistrement de l\'emprunt');
    }
  };

  return (
    <div className="recherche-container">
      <h1>Recherche de Livres</h1>
      
      <div className="search-bar">
        <input
          type="text"
          placeholder="Rechercher par titre, auteur ou ISBN..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <p>Chargement...</p>
      ) : (
        <div className="livres-grid">
          {filteredLivres.length === 0 ? (
            <p>Aucun livre trouvé</p>
          ) : (
            filteredLivres.map(livre => (
              <div key={livre.id} className="livre-card">
                <h3>{livre.titre}</h3>
                <p><strong>Auteur:</strong> {livre.auteur}</p>
                <p><strong>ISBN:</strong> {livre.isbn}</p>
                <p><strong>Année:</strong> {livre.annee_publication}</p>
                <p><strong>Catégorie:</strong> {livre.categorie}</p>
                <p className={livre.disponible ? 'disponible' : 'indisponible'}>
                  {livre.disponible ? '✓ Disponible' : '✗ Indisponible'}
                </p>
                {livre.disponible && (
                  <button 
                    onClick={() => handleEmprunt(livre.id)}
                    className="btn-emprunt"
                  >
                    Emprunter
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default Recherche;

