from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.tools import tool
load_dotenv()



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


system_prompt = """Tu es un assistant d'estimation de prix pour les biens immobiliers. Utilise les outils a ta disposition et n'invente aucune chiffre"""

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