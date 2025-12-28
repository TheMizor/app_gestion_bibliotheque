import React, { useState } from 'react';
import '../App.css';
import { authService } from '../services/authService';

function Authentification({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    nom: '',
    prenom: '',
    role: 'etudiant'
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      if (isLogin) {
        const response = await authService.login(formData.email, formData.password);
        onLogin(response.user);
      } else {
        await authService.register(formData);
        alert('Inscription réussie ! Vous pouvez maintenant vous connecter.');
        setIsLogin(true);
        setFormData({
          email: formData.email,
          password: '',
          nom: '',
          prenom: '',
          role: 'etudiant'
        });
      }
    } catch (err) {
      console.error('Erreur:', err);
      setError(err.message || 'Une erreur est survenue');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h1>{isLogin ? 'Connexion' : 'Inscription'}</h1>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <>
              <div className="form-group">
                <label>Nom *</label>
                <input
                  type="text"
                  name="nom"
                  value={formData.nom}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Prénom *</label>
                <input
                  type="text"
                  name="prenom"
                  value={formData.prenom}
                  onChange={handleChange}
                  required
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Mot de passe *</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              minLength="6"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Rôle *</label>
              <select
                name="role"
                value={formData.role}
                onChange={handleChange}
                required
              >
                <option value="etudiant">Étudiant</option>
                <option value="enseignant">Enseignant</option>
              </select>
            </div>
          )}

          <button type="submit" className="btn-submit">
            {isLogin ? 'Se connecter' : 'S\'inscrire'}
          </button>
        </form>

        <p className="toggle-auth">
          {isLogin ? (
            <>
              Pas encore de compte ?{' '}
              <span onClick={() => setIsLogin(false)}>S'inscrire</span>
            </>
          ) : (
            <>
              Déjà un compte ?{' '}
              <span onClick={() => setIsLogin(true)}>Se connecter</span>
            </>
          )}
        </p>
      </div>
    </div>
  );
}

export default Authentification;

