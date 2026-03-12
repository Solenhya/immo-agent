from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langsmith import traceable
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver  
from pydantic import BaseModel, Field
import json
import asyncio
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
    return f"Estimation du prix pour un {bien.type} de {bien.surface}m² avec {bien.rooms} pièces à {bien.location} : {prix}€ "


llm = ChatMistralAI(model="mistral-large-latest")


system_prompt = """Tu es un assistant d'estimation de prix pour les biens immobiliers. Utilise les outils a ta disposition et n'invente aucune chiffre"""

# Ajout du tool estimation_prix
tools = [estimation_prix]
agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt, checkpointer=InMemorySaver())
#agent_executor = AgentExecutor(agent=agent, tools=tools)
#@traceable
async def async_run_agent(user_message,thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    messages = {"messages":[{"role":"user", "content": user_message}]}
    result = await agent.ainvoke(messages, config=config)
    return result

async def async_run_agent_response(user_message, thread_id):
    result = await async_run_agent(user_message, thread_id)
    return result["messages"][-1].content

def get_state(thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    state = agent.get_state(config=config)
    return state