import asyncio
import sys
import os
from langsmith import traceable
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

from .runIA import (
    outil_dvf_historique, 
    outil_dvf_estimation, 
    outil_infos_ville,
    PROMPT_CENTRAL
)

# Configuration de l'agent
prompt = PROMPT_CENTRAL

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
import json

async def chat_loop(tools):
    print(f"🔧 Outils: {[t.name for t in tools]}")
    model_with_tools = model.bind_tools(tools)
    
    while True:
        try:
            print("\n👤 Question (ou 'exit') :")
            query = sys.stdin.readline().strip()
            if not query or query.lower() in ["exit", "q"]: break
            
            print("🤖 Analyse...")
            messages = [
                SystemMessage(content=prompt),
                HumanMessage(content=query)
            ]
            
            # 1. Appel du modèle
            response = await model_with_tools.ainvoke(messages)
            messages.append(response)
            
            # 2. Boucle d'outils (max 3)
            iterations = 0
            while response.tool_calls and iterations < 3:
                iterations += 1
                for tc in response.tool_calls:
                    print(f"🛠️ Appel : {tc['name']} {tc['args']}...")
                    tool = next(t for t in tools if t.name == tc['name'])
                    tool_output = await tool.ainvoke(tc['args'])
                    print(f"📥 Réponse ({len(str(tool_output))} chars)")
                    messages.append(ToolMessage(content=str(tool_output), tool_call_id=tc['id']))
                
                response = await model_with_tools.ainvoke(messages)
                messages.append(response)
            
            # 3. Synthèse si vide
            if not response.content:
                print("📝 Synthèse finale...")
                messages.append(HumanMessage(content="Affiche maintenant les résultats trouvés clairement."))
                response = await model_with_tools.ainvoke(messages)
            
            # 4. Affichage final
            if response.content:
                print(f"\n🏠 Agent : {response.content}")
            else:
                print("\n🏠 Agent : [Échec de la synthèse]")
                
        except Exception as e:
            print(f"❌ Erreur : {e}")
            if "rate_limit" in str(e).lower(): await asyncio.sleep(10)

@traceable
async def main():
    print("--- 🏠 AGENT IMMOBILIER (VERSION ACTION) ---")
    
    # On reste sur l'essentiel pour éviter de perdre le modèle 8B
    dvf_tools = [outil_dvf_historique, outil_dvf_estimation, outil_infos_ville]
    
    await chat_loop(dvf_tools)

if __name__ == "__main__":
    asyncio.run(main())
