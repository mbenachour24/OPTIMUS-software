import os
from dotenv import load_dotenv
import psycopg2

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion Render
DATABASE_URL = os.getenv("RENDER_DATABASE_URL")

# Connexion PostgreSQL
def get_db_connection():
    print(f"🔍 Tentative de connexion à la base de données avec l'URL : {DATABASE_URL}")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Connexion réussie à la base de données !")
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return None

# Tester la connexion
if __name__ == "__main__":
    connection = get_db_connection()
    if connection:
        connection.close()
        print("🔒 Connexion fermée correctement.")
    else:
        print("❌ Impossible de se connecter à la base de données.")
