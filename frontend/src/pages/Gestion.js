import React, { useState, useEffect } from 'react';
import '../App.css';

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
    disponible: true
  });

  useEffect(() => {
    fetchLivres();
  }, []);

  const fetchLivres = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/livres', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setLivres(data);
    } catch (error) {
      console.error('Erreur lors du chargement des livres:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const url = editMode 
      ? `http://localhost:5000/api/livres/${currentLivre.id}`
      : 'http://localhost:5000/api/livres';
    
    const method = editMode ? 'PUT' : 'POST';

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(currentLivre)
      });

      if (response.ok) {
        alert(editMode ? 'Livre modifié avec succès!' : 'Livre ajouté avec succès!');
        setShowModal(false);
        resetForm();
        fetchLivres();
      } else {
        const error = await response.json();
        alert(`Erreur: ${error.message}`);
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de l\'opération');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce livre ?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/livres/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        alert('Livre supprimé avec succès!');
        fetchLivres();
      } else {
        const error = await response.json();
        alert(`Erreur: ${error.message}`);
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la suppression');
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
                <td>
                  <span className={livre.disponible ? 'badge-disponible' : 'badge-indisponible'}>
                    {livre.disponible ? 'Disponible' : 'Emprunté'}
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

