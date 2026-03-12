import os
import requests
import sqlite3
import re
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool

load_dotenv()

model = ChatMistralAI(
    model="mistral-large-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0
)

# PROMPT CENTRAL PARTAGÉ (API & CLI)
PROMPT_CENTRAL = (
    "Tu es l'expert immobilier de Solenhya Immo.\n"
    "RÈGLES DE FONCTIONNEMENT :\n"
    "1. APPEL D'OUTILS (SILENCE TECHNIQUE) : Si tu as besoin de données, N'ÉCRIS RIEN D'AUTRE que l'appel d'outil. Silence total.\n"
    "2. DISTINCTION : Si on demande le prix de 'l'immobilier' sans préciser, appelle `outil_dvf_historique` deux fois : une pour 'Maison' et une pour 'Appartement'.\n"
    "3. EXCLUSION : Si on demande les 'ventes', ignore le prix moyen. Si on demande le 'prix moyen', ignore la liste des ventes.\n"
    "4. POLITESSE MIROIR : Ne dis 'Bonjour !' que si l'utilisateur l'a dit dans son message actuel.\n"
    "5. SYNTHÈSE : Rédige une phrase naturelle reprenant les données exactes."
)

@tool
def outil_dvf_historique(ville: str, type_bien: str = "Maison") -> str:
    """Consulte l'historique des ventes DVF pour une ville et un type de bien."""
    try:
        # Standardisation du nom de la ville
        v_search = ville.upper().replace('-', ' ').strip()
        v_alt = v_search.replace(' ', '-')
            
        conn = sqlite3.connect('data/immo_ventes.db')
        cursor = conn.cursor()
        query = """
            SELECT "Valeur fonciere", "Surface reelle bati", "Date mutation", "Voie"
            FROM transactions 
            WHERE (Commune = ? OR Commune = ? OR Commune LIKE ?)
            AND "Type local" = ? 
            AND "Valeur fonciere" > 1000 
            ORDER BY substr("Date mutation", 7, 4) DESC, substr("Date mutation", 4, 2) DESC, substr("Date mutation", 1, 2) DESC
            LIMIT 20
        """
        cursor.execute(query, [v_search, v_alt, f"{v_search}%", type_bien.capitalize()])
        rows = cursor.fetchall()
        conn.close()
        if not rows: return f"Aucun résultat trouvé pour {type_bien} à {ville}."
        res, t, c = "", 0, 0
        for r in rows: # On parcourt les résultats pour trouver les 5 meilleurs
            val, surf, date, voie = r
            if surf and surf > 0:
                p = val/surf
                if 800 < p < 15000:
                    if c < 5:
                        res += f"- {date}: {int(val)}€ ({int(surf)}m²) {voie}\n"
                    t += p; c += 1
        moy = round(t/c) if c > 0 else 0
        return f"Moyenne {type_bien}: {moy}€/m²\nVentes:\n{res if res else 'Pas de ventes cohérentes.'}"
    except Exception as e: return f"Erreur: {str(e)}"

def _get_average_price(ville: str, type_bien: str) -> int:
    try:
        v_search = ville.upper().replace('-', ' ').strip()
        v_alt = v_search.replace(' ', '-')
        
        conn = sqlite3.connect('data/immo_ventes.db')
        cursor = conn.cursor()
        query = """
            SELECT "Valeur fonciere", "Surface reelle bati"
            FROM transactions 
            WHERE (Commune = ? OR Commune = ? OR Commune LIKE ?)
            AND "Type local" = ? 
            AND "Valeur fonciere" > 1000
            ORDER BY substr("Date mutation", 7, 4) DESC, substr("Date mutation", 4, 2) DESC, substr("Date mutation", 1, 2) DESC
            LIMIT 50
        """
        cursor.execute(query, [v_search, v_alt, f"{v_search}%", type_bien.capitalize()])
        rows = cursor.fetchall()
        conn.close()
        t, c = 0, 0
        for r in rows:
            val, surf = r
            if surf and surf > 0:
                p = val/surf
                if 800 < p < 20000: # Plage un peu plus large pour les grandes villes
                    t += p; c += 1
        return round(t/c) if c > 0 else 0
    except:
        return 0

@tool
def outil_dvf_estimation(ville: str, surface: str, type_bien: str = "Maison", etat: str = "moyen") -> str:
    """Estime un prix. État : neuf, bon, moyen, a renover."""
    try:
        # Nettoyage de la surface (ex: "80 m2" -> 80)
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", str(surface).replace(',', '.'))
        surface_val = float(nums[0]) if nums else 0
    except:
        surface_val = 0
        
    if surface_val <= 0:
        return "Erreur: Veuillez préciser une surface valide (ex: 80)."

    p_m2 = _get_average_price(ville, type_bien)
    if not p_m2: return f"Données insuffisantes pour {type_bien} à {ville}."
    
    coeff = {"neuf": 1.2, "bon": 1.1, "moyen": 1.0, "a renover": 0.8}
    adj_coeff = coeff.get(etat.lower(), 1.0)
    val = surface_val * p_m2 * adj_coeff
    
    return f"**ESTIMATION : {int(val)} €**\n(Base: {p_m2}€/m² pour un bien en état {etat})"


@tool
def outil_infos_ville(ville: str) -> str:
    """Population."""
    try:
        url = "https://geo.api.gouv.fr/communes"
        res = requests.get(url, params={"nom": ville, "fields": "population", "limit": 1})
        d = res.json()
        return f"{ville}: {d[0]['population']} hab." if d else "Inconnu."
    except: return "Erreur."
