from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from pydantic import BaseModel
from app.services.agent import async_run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/api/chat")
async def chat_post(req: ChatRequest):
    try:
        # Appel à la fonction run_agent asynchrone
        # On utilise une session ("default") pour l'instant
        result = await async_run_agent(req.message, "default_session")
        
        # Le retour est généralement un dict avec une clé "messages" (langgraph)
        reply_content = ""
        if result and "messages" in result and len(result["messages"]) > 0:
            last_msg = result["messages"][-1]
            reply_content = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        else:
            reply_content = str(result)
            
        return {"reply": reply_content}
    except Exception as e:
        return {"reply": f"⚠️ Erreur côté serveur: {str(e)}"}
