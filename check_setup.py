#!/usr/bin/env python3
"""
Script de test pour vérifier que tout fonctionne
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=== Test Configuration ===\n")

# Test 1: GROQ_API_KEY
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    print(f"✅ GROQ_API_KEY configurée ({len(api_key)} chars)")
else:
    print("❌ GROQ_API_KEY manquante")
    print("   → Crée un fichier .env avec: GROQ_API_KEY=gsk_...")
    exit(1)

# Test 2: Base de données
import sqlite3
db_path = 'data/immo_ventes.db'
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Base de données DVF ({count} transactions)")
    except Exception as e:
        print(f"❌ Erreur BD: {e}")
        exit(1)
else:
    print(f"❌ Base de données manquante: {db_path}")
    exit(1)

# Test 3: Modules Python
try:
    from langchain_groq import ChatGroq
    print("✅ langchain-groq installé")
except:
    print("❌ langchain-groq manquant")
    exit(1)

try:
    import fastapi
    print("✅ fastapi installé")
except:
    print("❌ fastapi manquant")
    exit(1)

# Test 4: Outils DVF
try:
    from runIA import outil_dvf_historique, outil_dvf_estimation, outil_infos_ville
    print("✅ Outils DVF chargeables")
except Exception as e:
    print(f"❌ Erreur outils: {e}")
    exit(1)

print("\n=== ✅ Tout est prêt ! ===\n")
print("Lance l'API avec: python3 api.py")
print("Puis accède à: http://127.0.0.1:8000")
