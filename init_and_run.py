import db_session
import os

# 1. Créer le dossier data s'il n'existe pas
os.makedirs("data", exist_ok=True)

# 2. Initialiser la base d'authentification
print("🔧 Initialisation de la base de données auth...")
db_session.init_auth_db()
print("✅ Base de données prête.")
