import selectors
from langchain import tools
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langsmith import traceable
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
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
    
URL = "postgresql://admin:mdp@localhost:5432/ma_base_de_donnees"


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

#agent_executor = AgentExecutor(agent=agent, tools=tools)
config = {"configurable": {"thread_id": "1"}}
#@traceable
async def async_run_agent(user_message, thread_id, agent):
    messages = {"messages":[{"role":"user", "content": user_message}]}
    result = await agent.ainvoke(messages, config=config)
    return result

async def get_state(thread_id, agent):
    config = {"configurable": {"thread_id": thread_id}}
    state = await agent.aget_state(config=config)
    return state


async def cli_agent():
    async with AsyncPostgresSaver.from_conn_string(URL) as checkpointer:
        await checkpointer.setup()
        tools = [estimation_prix]
        agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt, checkpointer=checkpointer)
        while True:
            user_input = input("Entrez votre message (ou 'exit' pour quitter) : ")
            if user_input.lower() == "exit":
                print("Au revoir !")
                break
            if user_input.strip() == "":
                print("Veuillez entrer un message non vide.")
                continue
            if user_input.strip().lower() == "state":
                state = await get_state(thread_id="1", agent=agent)
                print("État actuel de l'agent :")
                print(state)
                continue

            result = await async_run_agent(user_input, thread_id="1", agent=agent)
            print("Résultat de l'agent :")
            content = result["messages"][-1].content
            print(content)


if __name__ == "__main__":
    loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(cli_agent())
    finally:
        loop.close()