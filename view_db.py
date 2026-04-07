#!/usr/bin/env python3
"""Script rapide pour voir les données de la BD."""

import sqlite3
import json

db_path = "data/immo_ventes.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("📊 COLONNES DE LA TABLE 'transactions'")
print("=" * 80)

cursor.execute("PRAGMA table_info(transactions)")
colonnes = cursor.fetchall()

for col in colonnes:
    col_id, col_name, col_type, _, _, _ = col
    print(f"  {col_id:2d}. {col_name:30s} ({col_type})")

print("\n" + "=" * 80)
print("🏠 EXEMPLES DE DONNÉES (5 premiers)")
print("=" * 80 + "\n")

cursor.execute("""
    SELECT 
        Commune,
        Voie,
        "Valeur fonciere",
        "Surface reelle bati",
        "Type local",
        latitude,
        longitude
    FROM transactions
    LIMIT 5
""")

for row in cursor.fetchall():
    commune, voie, prix, surface, type_bien, lat, lon = row
    print(f"📍 {commune} - {voie}")
    print(f"   Prix: {prix}€ | Surface: {surface}m² | Type: {type_bien}")
    print(f"   GPS: ({lat}, {lon})")
    print()

print("=" * 80)
print("🗺️  BIENS AVEC COORDONNÉES GPS")
print("=" * 80)

cursor.execute("""
    SELECT COUNT(*) FROM transactions WHERE latitude IS NOT NULL
""")
count_with_gps = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM transactions")
total = cursor.fetchone()[0]

print(f"\n✓ Biens avec GPS: {count_with_gps}/{total}")
print(f"  Couverture: {(count_with_gps/total*100):.1f}%\n")

# Afficher un exemple avec GPS
cursor.execute("""
    SELECT Commune, latitude, longitude 
    FROM transactions 
    WHERE latitude IS NOT NULL 
    LIMIT 3
""")

print("Exemples de biens géolocalisés:")
for commune, lat, lon in cursor.fetchall():
    print(f"  • {commune}: ({lat}, {lon})")

conn.close()

print("\n✅ Done!")
