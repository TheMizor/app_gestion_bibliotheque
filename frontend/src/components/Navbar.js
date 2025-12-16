import React from 'react';
import '../App.css';

function Navbar({ user, onLogout, onNavigate }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h2>📚 Bibliothèque</h2>
      </div>
      
      {user && (
        <>
          <div className="navbar-menu">
            <button onClick={() => onNavigate('recherche')} className="nav-link">
              Recherche
            </button>
            {user.role === 'bibliothecaire' && (
              <>
                <button onClick={() => onNavigate('gestion')} className="nav-link">
                  Gestion
                </button>
                <button onClick={() => onNavigate('dashboard')} className="nav-link">
                  Dashboard
                </button>
              </>
            )}
          </div>
          
          <div className="navbar-user">
            <span className="user-info">
              {user.prenom} {user.nom} ({user.role})
            </span>
            <button onClick={onLogout} className="btn-logout">
              Déconnexion
            </button>
          </div>
        </>
      )}
    </nav>
  );
}

export default Navbar;
