import React, { useState, useEffect } from 'react';
import '../App.css';
import { livreService } from '../services/livreService';

function Gestion() {
  const [livres, setLivres] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentLivre, setCurrentLivre] = useState({
    id: null,
    titre: '',
    auteur: '',
    isbn: '',
    annee_publication: '',
    categorie: '',
    nombre_exemplaires: 1,
    disponible: true
  });

  useEffect(() => {
    fetchLivres();
  }, []);

  const fetchLivres = async () => {
    try {
      const response = await livreService.getAllLivres();
      const livresData = response.books || response || [];
      if (Array.isArray(livresData)) {
        setLivres(livresData);
      } else {
        console.error('Format de données inattendu:', response);
        setLivres([]);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des livres:', error);
      setLivres([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editMode) {
        await livreService.updateLivre(currentLivre.id, currentLivre);
        alert('Livre modifié avec succès!');
      } else {
        await livreService.createLivre(currentLivre);
        alert('Livre ajouté avec succès!');
      }
      setShowModal(false);
      resetForm();
      fetchLivres();
    } catch (error) {
      console.error('Erreur:', error);
      alert(`Erreur: ${error.message || 'Erreur lors de l\'opération'}`);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce livre ?')) {
      return;
    }

    try {
      await livreService.deleteLivre(id);
      alert('Livre supprimé avec succès!');
      fetchLivres();
    } catch (error) {
      console.error('Erreur:', error);
      alert(`Erreur: ${error.message || 'Erreur lors de la suppression'}`);
    }
  };

  const handleEdit = (livre) => {
    setCurrentLivre(livre);
    setEditMode(true);
    setShowModal(true);
  };

  const handleAdd = () => {
    resetForm();
    setEditMode(false);
    setShowModal(true);
  };

  const resetForm = () => {
    setCurrentLivre({
      id: null,
      titre: '',
      auteur: '',
      isbn: '',
      annee_publication: '',
      categorie: '',
      nombre_exemplaires: 1,
      disponible: true
    });
  };

  return (
    <div className="gestion-container">
      <div className="gestion-header">
        <h1>Gestion des Livres</h1>
        <button onClick={handleAdd} className="btn-add">
          + Ajouter un livre
        </button>
      </div>

      <div className="livres-table">
        <table>
          <thead>
            <tr>
              <th>Titre</th>
              <th>Auteur</th>
              <th>ISBN</th>
              <th>Année</th>
              <th>Catégorie</th>
              <th>Exemplaires</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {livres.map(livre => (
              <tr key={livre.id}>
                <td>{livre.titre}</td>
                <td>{livre.auteur}</td>
                <td>{livre.isbn}</td>
                <td>{livre.annee_publication}</td>
                <td>{livre.categorie}</td>
                <td>{livre.exemplaires_disponibles !== undefined ? `${livre.exemplaires_disponibles} / ${livre.nombre_exemplaires}` : 'N/A'}</td>
                <td>
                  <span className={livre.exemplaires_disponibles > 0 ? 'badge-disponible' : 'badge-indisponible'}>
                    {livre.exemplaires_disponibles > 0 ? 'Disponible' : 'Indisponible'}
                  </span>
                </td>
                <td>
                  <button onClick={() => handleEdit(livre)} className="btn-edit">
                    Modifier
                  </button>
                  <button onClick={() => handleDelete(livre.id)} className="btn-delete">
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>{editMode ? 'Modifier le livre' : 'Ajouter un livre'}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Titre *</label>
                <input
                  type="text"
                  value={currentLivre.titre}
                  onChange={(e) => setCurrentLivre({...currentLivre, titre: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Auteur *</label>
                <input
                  type="text"
                  value={currentLivre.auteur}
                  onChange={(e) => setCurrentLivre({...currentLivre, auteur: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>ISBN *</label>
                <input
                  type="text"
                  value={currentLivre.isbn}
                  onChange={(e) => setCurrentLivre({...currentLivre, isbn: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Année de publication *</label>
                <input
                  type="number"
                  value={currentLivre.annee_publication}
                  onChange={(e) => setCurrentLivre({...currentLivre, annee_publication: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Catégorie *</label>
                <input
                  type="text"
                  value={currentLivre.categorie}
                  onChange={(e) => setCurrentLivre({...currentLivre, categorie: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Nombre d'exemplaires *</label>
                <input
                  type="number"
                  min="1"
                  value={currentLivre.nombre_exemplaires}
                  onChange={(e) => setCurrentLivre({...currentLivre, nombre_exemplaires: parseInt(e.target.value)})}
                  required
                />
              </div>
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    checked={currentLivre.disponible}
                    onChange={(e) => setCurrentLivre({...currentLivre, disponible: e.target.checked})}
                  />
                  Disponible
                </label>
              </div>
              <div className="modal-actions">
                <button type="submit" className="btn-submit">
                  {editMode ? 'Modifier' : 'Ajouter'}
                </button>
                <button type="button" onClick={() => setShowModal(false)} className="btn-cancel">
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Gestion;

