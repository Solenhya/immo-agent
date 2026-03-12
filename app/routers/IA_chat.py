from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.core.templating import templates
from pydantic import BaseModel
from app.services import agent
router = APIRouter()

class ChatRequest(BaseModel):
    message: str


@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return JSONResponse({"message": "Bienvenue sur la page de chat!"})

@router.post("/api/chat")
async def chat_post(request: Request, chat_request: ChatRequest):
    # Ici, tu peux traiter le message utilisateur
    retour = await agent.async_run_agent_response(chat_request.message, thread_id="default_thread")
    return JSONResponse({"message": retour})



@router.get("/conversation/{conversation_id}")
async def conversation_page(request: Request, conversation_id: str):

    # simulation DB
    messages = [
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Salut !"}
    ]

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
    if conversation_id == "123":
        return JSONResponse({"conversation_id": conversation_id, "messages": [
            {"role": "user", "content": "Quoi un messages?"},
            {"role": "assistant", "content": "Et oui un message secret"}
        ]})
    # simulation DB
    messages = [
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Salut !"}
    ]

    return JSONResponse({"conversation_id": conversation_id, "messages": messages})