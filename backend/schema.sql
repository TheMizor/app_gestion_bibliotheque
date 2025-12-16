CREATE DATABASE IF NOT EXISTS bibliotheque_db;
USE bibliotheque_db;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('bibliothecaire', 'etudiant', 'enseignant') NOT NULL DEFAULT 'etudiant',
    date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table des livres
CREATE TABLE IF NOT EXISTS livres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    auteur VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    nombre_exemplaires INT NOT NULL DEFAULT 1,
    exemplaires_disponibles INT NOT NULL DEFAULT 1,
    date_ajout DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_titre (titre),
    INDEX idx_auteur (auteur),
    INDEX idx_isbn (isbn)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table des emprunts
CREATE TABLE IF NOT EXISTS emprunts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livre_id INT NOT NULL,
    utilisateur_id INT NOT NULL,
    date_emprunt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_retour_prevue DATETIME NOT NULL,
    date_retour_reelle DATETIME NULL,
    statut ENUM('actif', 'retourne', 'en_retard') NOT NULL DEFAULT 'actif',
    FOREIGN KEY (livre_id) REFERENCES livres(id) ON DELETE CASCADE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    INDEX idx_livre (livre_id),
    INDEX idx_utilisateur (utilisateur_id),
    INDEX idx_statut (statut),
    INDEX idx_date_retour_prevue (date_retour_prevue)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO livres (titre, auteur, isbn, nombre_exemplaires, exemplaires_disponibles) VALUES 
    ("Harry Potter à l'école des sorciers", "J.K. Rowling", "978-2070584628", 5, 5),
    ("Le Seigneur des Anneaux : La Communauté de l'Anneau", "J.R.R. Tolkien", "978-2266286268", 3, 3),
    ("1984", "George Orwell", "978-2070368228", 4, 4),
    ("Le Petit Prince", "Antoine de Saint-Exupéry", "978-2070612758", 6, 6),
    ("L'Étranger", "Albert Camus", "978-2070360024", 4, 4),
    ("Dune", "Frank Herbert", "978-2266283045", 3, 3),
    ("Les Misérables", "Victor Hugo", "978-2070368229", 2, 2),
    ("Le Rouge et le Noir", "Stendhal", "978-2070413119", 3, 3),
    ("Madame Bovary", "Gustave Flaubert", "978-2070413118", 2, 2),
    ("Germinal", "Émile Zola", "978-2070413117", 3, 3),
    ("Python pour les Nuls", "John Paul Mueller", "978-2412050529", 2, 2),
    ("Clean Code", "Robert C. Martin", "978-0132350884", 2, 2),
    ("Design Patterns", "Erich Gamma", "978-0201633610", 1, 1),
    ("Introduction to Algorithms", "Thomas H. Cormen", "978-0262033848", 1, 1),
    ("The Pragmatic Programmer", "Andrew Hunt", "978-0201616224", 2, 2);