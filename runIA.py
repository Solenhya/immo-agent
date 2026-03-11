import os
import requests
import asyncio
import sqlite3
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from dataclasses import dataclass

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langsmith import traceable 

# Charge les variables d'environnement (.env)
load_dotenv()

# Configuration du modèle
model = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=1500
)


@dataclass
class Bien:
    type: str
    address: str
    surface: int

@tool
def geocode(adresse: str):
    """
    Géocode une adresse française pour obtenir ses coordonnées (latitude, longitude).
    :param adresse: L'adresse complète ou la ville.
    :return: les coordonnées [longitude, latitude]
    """
    URL = "https://data.geopf.fr/geocodage/search/"
    res = requests.get(URL, params={'q': adresse, 'limit': 1, 'autocomplete': 1})
    features = res.json().get('features')
    if features:
        return features[0].get('geometry').get('coordinates')
    return "Adresse non trouvée."

@tool
def infos_ville(ville: str) -> str:
    """
    Récupère des informations administratives et démographiques sur une ville (population, code postal, etc.).
    :param ville: Le nom de la ville.
    :return: Un résumé des informations de la ville.
    """
    print(f"\n🔎 [OUTIL LOCAL] Récupération des infos pour {ville}...")
    try:
        url = "https://geo.api.gouv.fr/communes"
        params = {
            "nom": ville,
            "fields": "nom,code,codesPostaux,population,codeDepartement",
            "format": "json",
            "limit": 1
        }
        res = requests.get(url, params=params)
        data = res.json()
        if data:
            info = data[0]
            nom = info.get('nom')
            pop = info.get('population', 'inconnue')
            cp = ", ".join(info.get('codesPostaux', []))
            dept = info.get('codeDepartement')
            res_str = f"Ville: {nom}, Population: {pop} habitants, Codes Postaux: {cp}, Département: {dept}."
            return res_str
        return f"Aucune information trouvée pour la ville {ville}."
    except Exception as e:
        return f"Erreur lors de la récupération des infos de la ville : {str(e)}"

@tool
def historique_ventes(ville: str, type_bien: str, pieces: int = None) -> str:
    """
    ESSENTIEL POUR L'ESTIMATION : Interroge la base locale sécurisée des transactions immobilières (DVF 2025).
    :param ville: Le nom exact de la commune (ex: TOULOUSE, PARIS, SAINT-CYR-SUR-LOIRE)
    :param type_bien: Le type de bien : 'Maison' ou 'Appartement'
    :param pieces: Le nombre de pièces principales (optionnel)
    :return: Le résumé des transactions récentes, ou un message d'erreur si rien n'est trouvé.
    """
    print(f"\n� [OUTIL LOCAL] Recherche dans la base DVF 2025 pour {type_bien} à {ville.upper()}...")
    try:
        conn = sqlite3.connect('data/immo_ventes.db')
        cursor = conn.cursor()
        
        # Requête de base
        requete = """
            SELECT "Valeur fonciere", "Surface reelle bati", "Date mutation"
            FROM transactions 
            WHERE Commune LIKE ? 
              AND "Type local" = ? 
              AND "Valeur fonciere" IS NOT NULL
              AND "Surface reelle bati" > 10
        """
        # Nettoyage du nom de la ville pour correspondre au format DVF (souvent avec des tirets)
        ville_clean = ville.upper().replace(' ', '-')
        params = [f"%{ville_clean}%", type_bien.capitalize()]
        
        # Ajout du filtre sur les pièces s'il est fourni
        if pieces is not None:
            requete += ' AND "Nombre pieces principales" = ?'
            params.append(pieces)
            
        cursor.execute(requete, params)
        resultats = cursor.fetchall()
        conn.close()
        
        if not resultats:
            return f"Aucune transaction récente trouvée à {ville} pour un(e) {type_bien}."
            
        # Calculs statistiques simples
        nb_ventes = len(resultats)
        prix_total = sum(row[0] for row in resultats)
        surface_totale = sum(row[1] for row in resultats)
        prix_m2_moyen = prix_total / surface_totale if surface_totale > 0 else 0
        
        return (f"J'ai analysé {nb_ventes} ventes de {type_bien} à {ville} en 2025. "
                f"Le prix moyen est de {round(prix_m2_moyen)} € le mètre carré. "
                "Utilise ces vrais chiffres pour formuler ton estimation à l'utilisateur.")
                
    except Exception as e:
        return f"Erreur lors de l'accès à la base de données : {str(e)}"
