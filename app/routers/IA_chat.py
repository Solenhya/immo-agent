from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from app.core.templating import templates
from pydantic import BaseModel
from app.services import agent, user_db_simple
import uuid


router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default_thread"  # Optionnel, pour gérer les conversations


@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return JSONResponse({"message": "Bienvenue sur la page de chat!"})

@router.post("/api/chat")
async def chat_post(request: Request, chat_request: ChatRequest):
    print(chat_request)
    user_id = request.cookies.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Utilisateur non authentifié"}, status_code=401)
    
    user_db_simple.add_conversation(user_id, conversation_id=chat_request.conversation_id) #ON ajoute ici la conversation car on ne veux pas ajouter de conversation vide
    # Ici, tu peux traiter le message utilisateur
    retour = await agent.async_run_agent_response(chat_request.message, thread_id=chat_request.conversation_id)
    return JSONResponse({"message": retour})

@router.get("/conversation")
async def dispatch_conversation(request: Request):
    conversation_id = str(uuid.uuid4())
    return RedirectResponse(url=f"/conversation/{conversation_id}")


@router.get("/conversation/{conversation_id}")
async def conversation_page(request: Request, conversation_id: str):
    
    messages = await agent.get_conversation(conversation_id)

    return templates.TemplateResponse(
        "conversation.html",
        {
            "request": request,
            "conversation_id": conversation_id,
            "messages": messages
        }
    )

@router.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    messages = await agent.get_conversation(conversation_id)
    return JSONResponse({"conversation_id": conversation_id, "messages": messages})

@router.get("/api/user/conversations")
async def get_my_conversations(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Utilisateur non authentifié"}, status_code=401)
    
    conversations = user_db_simple.get_user_conversations(user_id)
    return JSONResponse({"conversations": conversations})