from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langsmith import traceable
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver  
from langchain_mcp_adapters.interceptors import MCPToolCallRequest
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

#prompt = ChatPromptTemplate.from_messages([
#    ("system", "You are a data assistant using French open data."),
#    ("human", "{input}")
#])

system_prompt = """Tu es un assistant d'estimation de prix pour les biens immobiliers. Utilise les outils a ta disposition et n'invente aucune chiffre"""

# Ajout du tool estimation_prix
tools = [estimation_prix]
agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt, checkpointer=InMemorySaver())
#agent_executor = AgentExecutor(agent=agent, tools=tools)
config = {"configurable": {"thread_id": "1"}}
#@traceable
async def async_run_agent(user_message):
    messages = {"messages":[{"role":"user", "content": user_message}]}
    result = await agent.ainvoke(messages, config=config)
    return result


async def cli_agent():
    while True:
        user_input = input("Entrez votre message (ou 'exit' pour quitter) : ")
        if user_input.lower() == "exit":
            print("Au revoir !")
            break
        if user_input.strip() == "":
            print("Veuillez entrer un message non vide.")
            continue
        result = await async_run_agent(user_input)
        print("Résultat de l'agent :")
        content = result["messages"][-1].content
        print(content)


if __name__ == "__main__":
    asyncio.run(cli_agent())