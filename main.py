import asyncio
from langsmith import traceable
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from runIA import model, geocode, historique_ventes, infos_ville

@traceable
async def main():
    print("--- Initialisation de l'Agent Immobilier ---")
    
    mcp_tools = []
    
    # On essaie de se connecter au serveur distant
    try:
        async with streamable_http_client("https://mcp.data.gouv.fr/mcp") as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                mcp_tools = await load_mcp_tools(session)
                print("✅ Connexion à data.gouv.fr réussie")
                
                # IMPORTANT : Tout le reste du code de l'agent doit 
                # maintenant être à PEU PRÈS à ce niveau d'indentation, 
                # ou bien on sort les outils MCP de la fonction asynchrone pour les utiliser.
                
                # Pour éviter l'erreur de scope du "async with", on lance l'agent ici :
                tools = [geocode, historique_ventes, infos_ville] + mcp_tools
                await run_agent(tools)
                
    except Exception as e:
        print(f"⚠️ Impossible de joindre data.gouv.fr (Erreur: {e}). L'agent va démarrer avec les outils locaux uniquement.")
        tools = [geocode, historique_ventes, infos_ville]
        await run_agent(tools)

async def run_agent(tools):
    prompt = (
        "Tu es un expert en données publiques.\n"
        "Pour répondre à la question sur les risques (PPR), utilise UNIQUEMENT l'outil 'search_datasets' avec le mot 'PPR [ville]'."
    )
    
    agent = create_react_agent(model=model, tools=tools, prompt=prompt)
    
    query = "Quels sont les risques naturels et inondations (PPR) recensés à Paris ?"
    print(f"\n❓ Utilisateur : {query}\n")
    
    response = await agent.ainvoke({"messages": [("user", query)]})
    
    print("\n--- Réponse de l'Agent ---")
    for message in response["messages"]:
        if message.type == "ai" and message.content:
            print(message.content)

if __name__ == "__main__":
    asyncio.run(main())
