#!/usr/bin/env python3
"""Script pour géolocaliser les adresses et remplir latitude/longitude."""

import sqlite3
import requests
import time
from tqdm import tqdm

db_path = "data/immo_ventes.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer tous les biens sans coords
    cursor.execute("""
        SELECT rowid, Commune, Voie, 'Code postal'
        FROM transactions
        WHERE latitude IS NULL
        ORDER BY Commune
        LIMIT 100
    """)
    
    biens = cursor.fetchall()
    
    if not biens:
        print("✓ Tous les biens ont déjà des coordonnées !")
        exit(0)
    
    print(f"🌍 Géolocalisation de {len(biens)} biens...\n")
    
    for rowid, commune, voie, code_postal in tqdm(biens):
        try:
            # Construire l'adresse
            adresse = f"{voie}, {commune}"
            
            # Appeler l'API geo.api.gouv.fr (plus fiable pour France)
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
            
            # Rate limit: 1 requête par seconde max
            time.sleep(0.1)
            
        except Exception as e:
            print(f"\n⚠️ Erreur pour {commune}: {e}")
            continue
    
    conn.close()
    print("\n✅ Géolocalisation terminée !")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)
