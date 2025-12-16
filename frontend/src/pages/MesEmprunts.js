import React, { useState, useEffect } from 'react';
import '../App.css';
import { empruntService } from '../services/empruntService';
import { authService } from '../services/authService';

function MesEmprunts() {
  const [emprunts, setEmprunts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMesEmprunts();
  }, []);

  const fetchMesEmprunts = async () => {
    setLoading(true);
    try {
      const user = authService.getCurrentUser();
      if (user) {
        // Supposons que l'API permet de récupérer les emprunts de l'utilisateur connecté
        // ou via son ID. Le service empruntService a getEmpruntsByUser.
        const response = await empruntService.getEmpruntsByUser(user.id);
        const data = response.loans || response.borrowings || response || [];
        
        // Trier : non retournés en premier, puis par date de retour prévue
        const sortedData = Array.isArray(data) ? data.sort((a, b) => {
          if (a.date_retour_reelle && !b.date_retour_reelle) return 1;
          if (!a.date_retour_reelle && b.date_retour_reelle) return -1;
          return new Date(a.date_retour_prevue) - new Date(b.date_retour_prevue);
        }) : [];
        
        setEmprunts(sortedData);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des emprunts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRetour = async (empruntId) => {
    if (!window.confirm('Voulez-vous vraiment retourner ce livre ?')) {
      return;
    }

    try {
      await empruntService.returnLivre(empruntId);
      alert('Livre retourné avec succès !');
      fetchMesEmprunts(); // Rafraîchir la liste
    } catch (error) {
      console.error('Erreur lors du retour:', error);
      alert(`Erreur: ${error.message || 'Impossible de retourner le livre'}`);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
  };

  const isEnRetard = (dateRetourPrevue, dateRetourReelle) => {
    if (dateRetourReelle) return false;
    return new Date(dateRetourPrevue) < new Date();
  };

  return (
    <div className="gestion-container">
      <h1>Mes Emprunts</h1>

      {loading ? (
        <p>Chargement...</p>
      ) : (
        <div className="livres-table">
          <table>
            <thead>
              <tr>
                <th>Livre</th>
                <th>Date d'emprunt</th>
                <th>A rendre avant le</th>
                <th>Date de retour</th>
                <th>Statut</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {emprunts.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{textAlign: 'center'}}>Aucun emprunt en cours ou historique vide.</td>
                </tr>
              ) : (
                emprunts.map(emprunt => (
                  <tr key={emprunt.id} className={emprunt.date_retour_reelle ? 'row-returned' : ''}>
                    <td>{emprunt.book_title || emprunt.livre_titre || 'Titre inconnu'}</td>
                    <td>{formatDate(emprunt.date_emprunt)}</td>
                    <td>{formatDate(emprunt.date_retour_prevue)}</td>
                    <td>{emprunt.date_retour_reelle ? formatDate(emprunt.date_retour_reelle) : '-'}</td>
                    <td>
                      {emprunt.date_retour_reelle ? (
                        <span className="badge-retourne">Retourné</span>
                      ) : isEnRetard(emprunt.date_retour_prevue, emprunt.date_retour_reelle) ? (
                        <span className="badge-retard">En retard</span>
                      ) : (
                        <span className="badge-en-cours">En cours</span>
                      )}
                    </td>
                    <td>
                      {!emprunt.date_retour_reelle && (
                        <button 
                          onClick={() => handleRetour(emprunt.id)}
                          className="btn-retour"
                        >
                          Restituer
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default MesEmprunts;

