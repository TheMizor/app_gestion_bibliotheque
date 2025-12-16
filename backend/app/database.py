"""
Configuration et connexion à la base de données MySQL
"""
import mysql.connector
from mysql.connector import Error
from config import Config


class Database:
    """Gestionnaire de connexion à la base de données"""
    
    def __init__(self):
        self.connection = None
        self.config = Config()
    
    def connect(self):
        """Établir la connexion à la base de données"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config.MYSQL_HOST,
                port=self.config.MYSQL_PORT,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD,
                database=self.config.MYSQL_DATABASE
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Erreur de connexion à MySQL: {e}")
            return False
    
    def disconnect(self):
        """Fermer la connexion à la base de données"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def get_connection(self):
        """Récupérer la connexion active"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                raise ConnectionError("Impossible de se connecter à la base de données MySQL")
        return self.connection
    
    def execute_query(self, query, params=None):
        """Exécuter une requête SQL"""
        try:
            cursor = self.get_connection().cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor
        except Error as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            raise
    
    def commit(self):
        """Valider les transactions"""
        if self.connection:
            self.connection.commit()

