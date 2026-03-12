import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
import json

from runIA import (
    model, 
    outil_dvf_historique, 
    outil_dvf_estimation, 
    outil_infos_ville,
    PROMPT_CENTRAL
)

app = FastAPI(title="Solenhya Immo Agent API")

prompt = PROMPT_CENTRAL


dvf_tools = [outil_dvf_historique, outil_dvf_estimation, outil_infos_ville]
model_with_tools = model.bind_tools(dvf_tools)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=req.message)
        ]
        
        response = await model_with_tools.ainvoke(messages)
        messages.append(response)
        
        # Exécution des outils avec protection contre les répétitions
        iterations = 0
        latest_tool_results = {} # name -> content
        
        while response.tool_calls and iterations < 5:
            iterations += 1
            for tc in response.tool_calls:
                try:
                    tool_name = tc['name']
                    tool = next((t for t in dvf_tools if t.name == tool_name), None)
                    if tool:
                        output = await tool.ainvoke(tc['args'])
                        latest_tool_results[tool_name] = str(output)
                        messages.append(ToolMessage(content=str(output), tool_call_id=tc['id']))
                    else:
                        messages.append(ToolMessage(content=f"Erreur: Outil {tool_name} inconnu.", tool_call_id=tc['id']))
                except Exception as e:
                    messages.append(ToolMessage(content=f"Erreur tool: {str(e)}", tool_call_id=tc['id']))
            
            response = await model_with_tools.ainvoke(messages)
            messages.append(response)
        
        # Construction de la réponse finale
        # On laisse le LLM faire la synthèse demandée (phrases naturelles, reprise des termes)
        if response.content and len(response.content.strip()) > 5:
            final_text = response.content
        elif latest_tool_results:
            # Fallback si le LLM n'a fait que l'appel d'outil sans phrase finale
            final_text = "\n\n".join(latest_tool_results.values())
        else:
            final_text = "Je n'ai pas trouvé de données correspondantes dans la base DVF."
            
        return {"reply": final_text}
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return {"reply": f"Erreur : {str(e)}"}


os.makedirs("frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
