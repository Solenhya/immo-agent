import sqlite3
import pandas as pd
import os

# Chemins des fichiers
CSV_FILE = 'data/ValeursFoncieres-2025-S1.csv'
DB_FILE = 'data/immo_ventes.db'

def create_database():
    print(f"Création de la base de données {DB_FILE}...")
    
    # 1. Connexion à la future base (crée le fichier s'il n'existe pas)
    conn = sqlite3.connect(DB_FILE)
    
    # 2. Lecture du CSV (par paquets de 50 000 lignes pour ne pas faire planter l'ordi)
    print(f"Lecture du fichier: {CSV_FILE}")
    
    # On précise que le séparateur est | (typiques des DVF) et on garde que l'essentiel
    cols_utiles = ['Date mutation', 'Valeur fonciere', 'No voie', 'Type de voie', 'Voie', 
                   'Code postal', 'Commune', 'Type local', 'Surface reelle bati', 'Nombre pieces principales']
                   
    chunksize = 50000
    for chunk in pd.read_csv(CSV_FILE, sep=',', usecols=cols_utiles, low_memory=False, chunksize=chunksize):
        
        # 3. Nettoyage des chiffres (enlever la virgule pour que Python comprenne)
        chunk['Valeur fonciere'] = chunk['Valeur fonciere'].astype(str).str.replace(',', '.').astype(float)
        chunk['Surface reelle bati'] = chunk['Surface reelle bati'].astype(str).str.replace(',', '.').astype(float)
        
        # 4. Sauvegarde dans la base SQLite (dans une table appelée "transactions")
        chunk.to_sql('transactions', conn, if_exists='append', index=False)
        print(f"  + {chunk.shape[0]} lignes ajoutées...")

    # 5. Création d'index pour accélérer les recherches de l'agent
    print("Création des index (sur Commune et Code Postal) pour une recherche ultra-rapide...")
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX idx_commune ON transactions(Commune);")
    cursor.execute("CREATE INDEX idx_cp ON transactions(`Code postal`);")
    
    conn.commit()
    conn.close()
    
    print("Terminé ! Prenez un café, votre base SQLite est prête à être utilisée par l'IA.")

if __name__ == "__main__":
    create_database()
