from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.tools import tool
load_dotenv()


class HistoriqueVentesInput(BaseModel):
    """Input for historical sales data queries."""
    location: str = Field(description="City name or coordinates")
    years: int = Field(description="Number of past years to consider")

class BienSimilairesInput(BaseModel):
    """Input for searching similar properties within a range."""
    ville: str = Field(description="City name")
    surface_min: float = Field(description="Minimum surface area in square meters")
    surface_max: float = Field(description="Maximum surface area in square meters")
    type_bien: str = Field(description="Type of property (maison or appartement)")
    rayon_km: float = Field(description="Radius in kilometers to consider", default=10)

@tool
def historique_ventes(input: HistoriqueVentesInput):
    """Récupère l'historique des ventes immobilières pour une localisation donnée et une période spécifiée.
    Args:
        input (HistoriqueVentesInput): Les critères de recherche pour l'historique des ventes.
    Returns:
        list: Une liste d'enregistrements de ventes immobilières correspondant aux critères.
    """
    # Simuler une réponse de la base de données DVF
    ventes = [
        {"location": input.location, "surface": 70, "rooms": 3, "type": "appartement", "price": 350000, "date": "2023-05-10"},
        {"location": input.location, "surface": 120, "rooms": 5, "type": "maison", "price": 600000, "date": "2022-11-20"},
        # ... plus de données simulées
    ]
    return json.dumps(ventes)

@tool
def biens_similaires(params: BienSimilairesInput):
    """Trouve des biens immobiliers similaires dans un périmètre donné.
    
    Cherche les biens qui ont la même surface (±10%) et le même type
    à moins de X km de la ville spécifiée.
    """
    import sqlite3
    import requests
    from math import radians, cos, sin, asin, sqrt
    
    # ÉTAPE 1: Récupérer les coordonnées de la ville
    try:
        response = requests.get(
            "https://geo.api.gouv.fr/communes",
            params={"nom": params.ville, "limit": 1}
        )
        data = response.json()
        if not data:
            return f"❌ Ville '{params.ville}' non trouvée"
        
        ref_lat = data[0]["centre"]["coordinates"][1]
        ref_lon = data[0]["centre"]["coordinates"][0]
    except Exception as e:
        return f"❌ Erreur géolocalisation: {e}"
    
    # ÉTAPE 2: Chercher en BD les biens similaires
    try:
        conn = sqlite3.connect("data/immo_ventes.db")
        cursor = conn.cursor()
        
        # Biens avec surface similaire (±10%)
        cursor.execute("""
            SELECT 
                Commune,
                Voie,
                "Valeur fonciere",
                "Surface reelle bati",
                latitude,
                longitude
            FROM transactions
            WHERE "Type local" = ?
            AND "Surface reelle bati" BETWEEN ? AND ?
            AND latitude IS NOT NULL
            AND longitude IS NOT NULL
            LIMIT 100
        """, [
            params.type_bien.capitalize(),
            params.surface_min * 0.9,
            params.surface_max * 1.1
        ])
        
        biens = cursor.fetchall()
        conn.close()
        
        if not biens:
            return f"❌ Aucun {params.type_bien} trouvé avec surface {params.surface_min}-{params.surface_max}m²"
        
        # ÉTAPE 3: Calculer les distances et filtrer
        biens_proches = []
        
        for commune, voie, prix, surface, lat, lon in biens:
            # Formule Haversine
            lat1, lon1, lat2, lon2 = map(radians, [ref_lat, ref_lon, lat, lon])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            distance = c * 6371  # Rayon Terre en km
            
            # Garder seulement ceux dans le rayon
            if distance <= params.rayon_km:
                biens_proches.append({
                    "commune": commune,
                    "adresse": voie,
                    "prix": prix,
                    "surface": surface,
                    "distance": round(distance, 1)
                })
        
        # ÉTAPE 4: Retourner résultats formatés
        if not biens_proches:
            return f"❌ Aucun {params.type_bien} à {params.surface_min}-{params.surface_max}m² dans {params.rayon_km}km"
        
        # Trier par distance
        biens_proches.sort(key=lambda x: x["distance"])
        
        # Formatter le texte pour le LLM
        resultat = f"✅ Trouvé {len(biens_proches)} {params.type_bien}(s) similaire(s) à {params.rayon_km}km de {params.ville}:\n\n"
        
        for i, bien in enumerate(biens_proches[:10], 1):
            resultat += f"{i}. {bien['commune']} - {bien['adresse']}\n"
            resultat += f"   💰 {int(bien['prix'])}€ | 📐 {bien['surface']}m² | 📍 {bien['distance']}km\n\n"
        
        if len(biens_proches) > 10:
            resultat += f"... et {len(biens_proches) - 10} autres"
        
        return resultat
        
    except Exception as e:
        return f"❌ Erreur BD: {str(e)}"


class BienImmobilier(BaseModel):
    """Input for real estate queries."""
    location: str = Field(description="City name or coordinates")
    surface : float = Field(description="Surface area in square meters")
    rooms: int = Field(description="Number of rooms")
    type : str = Field(description="maison ou appartement")
    


@tool
def estimation_prix(bien: BienImmobilier):
    """Estime le prix d'un bien immobilier en fonction de sa localisation, sa surface, son nombre de pièces et son type (maison ou appartement).
    Args:
        bien (BienImmobilier): Les caractéristiques du bien immobilier à estimer.
    Returns:
        float: Une estimation du prix du bien immobilier.
    """
    prix = bien.surface * 5000
    if bien.type == "maison":
        prix *= 1.2

    return prix


def format_messages(lc_messages):
    role_map = {
        "human": "user",
        "ai": "assistant",
        "system": "system"
    }

    return [
        {
            "role": role_map.get(m.type, m.type),
            "content": m.content
        }
        for m in lc_messages
    ]



system_prompt = """Tu es un assistant expert en biens immobiliers. Tu aides l'utilisateur à rechercher des propriétés, estimer des prix et trouver des biens similaires.

📋 RÈGLES IMPORTANTES :
1. Utilise TOUJOURS les outils disponibles pour répondre aux requêtes (estimation_prix, historique_ventes, biens_similaires)
2. N'invente JAMAIS de chiffres ou de prix
3. Si l'utilisateur ne mentionne pas une ville dans sa requête actuelle, utilise AUTOMATIQUEMENT la DERNIÈRE VILLE mentionnée dans la conversation
4. Mémorise chaque nouvelle ville mentionnée pour les requêtes futures
5. Si aucune ville n'a été mentionnée, demande-la avant de rechercher

📍 EXEMPLE :
- L'utilisateur dit : "Je cherche une maison à Tours"
- Ensuite : "Je cherche une maison de 100m² dans un rayon de 120km"
- → Tu dois utiliser Tours automatiquement, car c'est la dernière ville mentionnée"""


llm = ChatMistralAI(model="mistral-large-latest")


tools = [estimation_prix]

class AgentSingleton:
    _instance = None

    @classmethod
    def initialize(cls, checkpointer):
        """À appeler une seule fois au démarrage de l'application (lifespan)."""
        if cls._instance is None:
            cls._instance = create_agent(
                model=llm,
                tools=tools,
                system_prompt=system_prompt,
                checkpointer=checkpointer
            )
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("AgentSingleton non initialisé. Appelez initialize() depuis le lifespan.")
        return cls._instance

    @classmethod
    def reset(cls):
        """Réinitialise le singleton (utile pour les tests)."""
        cls._instance = None


async def async_run_agent(user_message, thread_id):
    agent = AgentSingleton.get_instance()
    config = {"configurable": {"thread_id": thread_id}}
    messages = {"messages": [{"role": "user", "content": user_message}]}
    result = await agent.ainvoke(messages, config=config)
    return result

async def async_run_agent_response(user_message, thread_id):
    result = await async_run_agent(user_message, thread_id)
    return result["messages"][-1].content

async def get_state(thread_id):
    agent = AgentSingleton.get_instance()
    config = {"configurable": {"thread_id": thread_id}}
    state = await agent.aget_state(config=config)
    return state

async def get_conversation(thread_id):
    state = await get_state(thread_id)
    if state and "messages" in state.values:
        print(state)
        messages = state.values["messages"]
        messages = format_messages(messages)
        return messages
    else:
        return []
    
async def delete_thread(thread_id):
    agent = AgentSingleton.get_instance()
    await agent.checkpointer.adelete_thread(thread_id=thread_id)