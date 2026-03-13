import psycopg2
import os
import uuid
import pandas as pd

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
) 

CSV_FILE = 'data/ValeursFoncieres-2025-S1.csv'
def create_data_table():
    with conn.cursor() as cur:
        cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    date_mutation DATE,
    valeur_fonciere FLOAT,
    no_voie TEXT,
    type_de_voie TEXT,
    voie TEXT,
    code_postal TEXT,
    commune TEXT,
    type_local TEXT,
    surface_reelle_bati FLOAT,
    nombre_pieces_principales FLOAT
);""")
        conn.commit()

def create_database_DVF():
    print(f"Création de la base de données DVF...")
    
    # 1. Connexion à la future base (crée le fichier s'il n'existe pas)
    
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


from sqlalchemy import create_engine

CSV_FILE = "data/ValeursFoncieres-2025-S1.csv"

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

def create_database_DVF_2():

    print("Création de la base DVF...")
    print(f"Lecture du fichier: {CSV_FILE}")

    cols_utiles = [
        'Date mutation', 'Valeur fonciere', 'No voie', 'Type de voie', 'Voie',
        'Code postal', 'Commune', 'Type local', 'Surface reelle bati',
        'Nombre pieces principales'
    ]

    chunksize = 50000

    for chunk in pd.read_csv(
        CSV_FILE,
        sep=',',
        usecols=cols_utiles,
        low_memory=False,
        chunksize=chunksize
    ):

        chunk['Valeur fonciere'] = pd.to_numeric(
            chunk['Valeur fonciere'].astype(str).str.replace(',', '.'),
            errors='coerce'
        )

        chunk['Surface reelle bati'] = pd.to_numeric(
            chunk['Surface reelle bati'].astype(str).str.replace(',', '.'),
            errors='coerce'
        )

        chunk.to_sql('transactions', engine, if_exists='append', index=False)

        print(f"+ {chunk.shape[0]} lignes ajoutées")