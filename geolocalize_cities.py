#!/usr/bin/env python3
"""Géolocaliser les biens pour 3 villes: Tours, Paris, Bordeaux."""

import sqlite3
import requests
import time
from tqdm import tqdm

db_path = "data/immo_ventes.db"
villes_cibles = ["TOURS"]

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer les biens sans coords pour Tours
    query = """
        SELECT rowid, Commune, Voie
        FROM transactions
        WHERE latitude IS NULL
        AND Commune = ?
        LIMIT 2000
    """
    
    cursor.execute(query, villes_cibles)
    biens = cursor.fetchall()
    
    print(f"🌍 Géolocalisation de {len(biens)} biens pour : {', '.join(villes_cibles)}\n")
    
    if not biens:
        print("✓ Aucun bien à géolocaliser pour ces villes")
        exit(0)
    
    success = 0
    failed = 0
    
    for rowid, commune, voie in tqdm(biens):
        try:
            # Construire l'adresse
            adresse = f"{voie}, {commune}"
            
            # Appeler l'API
            response = requests.get(
                "https://api-adresse.data.gouv.fr/search/",
                params={"q": adresse, "limit": 1}
            )
            
            data = response.json()
            
            if data.get("features"):
                coords = data["features"][0]["geometry"]["coordinates"]
                lon, lat = coords[0], coords[1]
                
                # Mettre à jour la BD
                cursor.execute("""
                    UPDATE transactions
                    SET latitude = ?, longitude = ?
                    WHERE rowid = ?
                """, [lat, lon, rowid])
                conn.commit()
                success += 1
            else:
                failed += 1
            
            # Rate limit
            time.sleep(0.05)
            
        except Exception as e:
            failed += 1
            continue
    
    conn.close()
    
    print(f"\n✅ Géolocalisation terminée !")
    print(f"   Succès: {success}")
    print(f"   Échecs: {failed}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)
