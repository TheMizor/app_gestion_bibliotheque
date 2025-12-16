import React, { useState, useEffect } from 'react';
import '../App.css';

function Dashboard() {
  const [stats, setStats] = useState({
    total_livres: 0,
    livres_disponibles: 0,
    livres_empruntes: 0,
    total_emprunts: 0,
    emprunts_actifs: 0,
    emprunts_retard: 0
  });
  const [empruntsRecents, setEmpruntsRecents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Récupérer les statistiques
      const statsResponse = await fetch('http://localhost:5000/api/dashboard/stats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const statsData = await statsResponse.json();
      setStats(statsData);

      // Récupérer les emprunts récents
      const empruntsResponse = await fetch('http://localhost:5000/api/emprunts?limit=10', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const empruntsData = await empruntsResponse.json();
      setEmpruntsRecents(empruntsData);
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRetour = async (empruntId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/emprunts/${empruntId}/retour`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        alert('Retour enregistré avec succès!');
        fetchDashboardData();
      } else {
        const error = await response.json();
        alert(`Erreur: ${error.message}`);
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de l\'enregistrement du retour');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
  };

  const isRetard = (dateRetourPrevue) => {
    const today = new Date();
    const dateRetour = new Date(dateRetourPrevue);
    return dateRetour < today;
  };

  if (loading) {
    return <div className="dashboard-container"><p>Chargement...</p></div>;
  }

  return (
    <div className="dashboard-container">
      <h1>Tableau de Bord - Bibliothécaire</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Livres</h3>
          <p className="stat-number">{stats.total_livres}</p>
        </div>
        <div className="stat-card">
          <h3>Livres Disponibles</h3>
          <p className="stat-number disponible">{stats.livres_disponibles}</p>
        </div>
        <div className="stat-card">
          <h3>Livres Empruntés</h3>
          <p className="stat-number emprunte">{stats.livres_empruntes}</p>
        </div>
        <div className="stat-card">
          <h3>Total Emprunts</h3>
          <p className="stat-number">{stats.total_emprunts}</p>
        </div>
        <div className="stat-card">
          <h3>Emprunts Actifs</h3>
          <p className="stat-number">{stats.emprunts_actifs}</p>
        </div>
        <div className="stat-card">
          <h3>Emprunts en Retard</h3>
          <p className="stat-number retard">{stats.emprunts_retard}</p>
        </div>
      </div>

      <div className="emprunts-section">
        <h2>Emprunts Récents</h2>
        <div className="emprunts-table">
          <table>
            <thead>
              <tr>
                <th>Utilisateur</th>
                <th>Livre</th>
                <th>Date Emprunt</th>
                <th>Date Retour Prévue</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {empruntsRecents.length === 0 ? (
                <tr>
                  <td colSpan="6">Aucun emprunt récent</td>
                </tr>
              ) : (
                empruntsRecents.map(emprunt => (
                  <tr key={emprunt.id} className={isRetard(emprunt.date_retour_prevue) && !emprunt.date_retour_effective ? 'retard' : ''}>
                    <td>{emprunt.utilisateur_nom}</td>
                    <td>{emprunt.livre_titre}</td>
                    <td>{formatDate(emprunt.date_emprunt)}</td>
                    <td>{formatDate(emprunt.date_retour_prevue)}</td>
                    <td>
                      {emprunt.date_retour_effective ? (
                        <span className="badge-retourne">Retourné</span>
                      ) : isRetard(emprunt.date_retour_prevue) ? (
                        <span className="badge-retard">En retard</span>
                      ) : (
                        <span className="badge-en-cours">En cours</span>
                      )}
                    </td>
                    <td>
                      {!emprunt.date_retour_effective && (
                        <button 
                          onClick={() => handleRetour(emprunt.id)}
                          className="btn-retour"
                        >
                          Enregistrer retour
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

