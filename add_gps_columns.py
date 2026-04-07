#!/usr/bin/env python3
"""Script pour ajouter les colonnes latitude et longitude à la BD."""

import sqlite3
import os

db_path = "data/immo_ventes.db"

if not os.path.exists(db_path):
    print(f"❌ BD non trouvée: {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer le schéma actuel
    cursor.execute("PRAGMA table_info(transactions)")
    colonnes = [col[1] for col in cursor.fetchall()]
    
    print(f"📊 Colonnes existantes: {colonnes}\n")
    
    # Ajouter latitude si elle n'existe pas
    if "latitude" not in colonnes:
        print("➕ Ajout colonne: latitude")
        cursor.execute("ALTER TABLE transactions ADD COLUMN latitude FLOAT")
        print("✅ Colonne latitude ajoutée")
    else:
        print("✓ Colonne latitude existe déjà")
    
    # Ajouter longitude si elle n'existe pas
    if "longitude" not in colonnes:
        print("➕ Ajout colonne: longitude")
        cursor.execute("ALTER TABLE transactions ADD COLUMN longitude FLOAT")
        print("✅ Colonne longitude ajoutée")
    else:
        print("✓ Colonne longitude existe déjà")
    
    conn.commit()
    conn.close()
    
    print("\n✅ BD mise à jour avec succès !")
    
except sqlite3.OperationalError as e:
    print(f"❌ Erreur: {e}")
    print("   → La table 'transactions' n'existe peut-être pas")
    print("   → Vérifiez le nom exact de votre table dans la BD")
    exit(1)
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)
