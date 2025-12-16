import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Recherche from './pages/Recherche';
import Gestion from './pages/Gestion';
import Dashboard from './pages/Dashboard';
import Authentification from './pages/Authentification';
import { authService } from './services/authService';

function App() {
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('recherche');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Vérifier si l'utilisateur est déjà connecté
    const storedUser = authService.getCurrentUser();
    if (storedUser) {
      setUser(storedUser);
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setCurrentPage('recherche');
  };

  const handleLogout = () => {
    authService.logout();
    setUser(null);
    setCurrentPage('recherche');
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    if (!user) {
      return <Authentification onLogin={handleLogin} />;
    }

    switch (currentPage) {
      case 'recherche':
        return <Recherche />;
      case 'gestion':
        return user.role === 'bibliothecaire' ? <Gestion /> : <Recherche />;
      case 'dashboard':
        return user.role === 'bibliothecaire' ? <Dashboard /> : <Recherche />;
      default:
        return <Recherche />;
    }
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading-container">
          <p>Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <Navbar 
        user={user} 
        onLogout={handleLogout} 
        onNavigate={handleNavigate}
      />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
