# Fichier : agent_memory.py
import os
import sqlite3
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
from langchain_mistralai import ChatMistralAI
from .runIA import outil_dvf_historique, outil_dvf_estimation, outil_infos_ville, PROMPT_CENTRAL

load_dotenv()

model = ChatMistralAI(model="mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY"), temperature=0)

# On ajoute la règle de rappel
PROMPT_MEMOIRE = PROMPT_CENTRAL + (
    "\n\n6. RÈGLE DE MÉMOIRE : Tu as accès à l'historique de la discussion. "
    "Si l'utilisateur pose une question répétée, mentionne poliment que c'est un rappel."
)

conn = sqlite3.connect("data/memory.db", check_same_thread=False)
memory = SqliteSaver(conn)

dvf_tools = [outil_dvf_historique, outil_dvf_estimation, outil_infos_ville]

# 💡 CORRECTION : Utilisation de l'argument 'prompt' (version actuelle de langgraph)
agent_executor = create_react_agent(
    model, 
    tools=dvf_tools, 
    checkpointer=memory, 
    prompt=PROMPT_MEMOIRE
)

def interroger_agent(message_utilisateur: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    resultat = agent_executor.invoke({"messages": [("user", message_utilisateur)]}, config=config)
    return resultat["messages"][-1].content
