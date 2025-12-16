import React, { useState, useEffect } from 'react';
import '../App.css';
import { livreService } from '../services/livreService';
import { empruntService } from '../services/empruntService';

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
      // Vérifier que livres est bien un tableau avant de filtrer
      if (!Array.isArray(livres)) return;
      
      const filtered = livres.filter(livre =>
        (livre.titre && livre.titre.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (livre.auteur && livre.auteur.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (livre.isbn && livre.isbn.includes(searchTerm))
      );
      setFilteredLivres(filtered);
    }
  }, [searchTerm, livres]);

  const fetchLivres = async () => {
    setLoading(true);
    try {
      const response = await livreService.getAllLivres();
      // Le backend retourne { books: [...], total: ... } ou directement [...]
      const livresData = response.books || response || [];
      
      if (Array.isArray(livresData)) {
        setLivres(livresData);
        setFilteredLivres(livresData);
      } else {
        console.error('Format de données inattendu:', response);
        setLivres([]);
        setFilteredLivres([]);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des livres:', error);
      setLivres([]);
      setFilteredLivres([]);
    } finally {
      setLoading(false);
    }
  };

  const handleEmprunt = async (livreId) => {
    try {
      // Le backend attend 'book_id'
      await empruntService.createEmprunt({ book_id: livreId });
      alert('Emprunt enregistré avec succès !');
      fetchLivres(); // Recharger la liste
    } catch (error) {
      console.error('Erreur lors de l\'emprunt:', error);
      alert(`Erreur: ${error.message || 'Erreur lors de l\'enregistrement de l\'emprunt'}`);
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
                <p><strong>Exemplaires:</strong> {livre.exemplaires_disponibles !== undefined ? `${livre.exemplaires_disponibles} / ${livre.nombre_exemplaires}` : 'N/A'}</p>
                <p className={livre.exemplaires_disponibles > 0 ? 'disponible' : 'indisponible'}>
                  {livre.exemplaires_disponibles > 0 ? '✓ Disponible' : '✗ Indisponible'}
                </p>
                {livre.exemplaires_disponibles > 0 && (
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

