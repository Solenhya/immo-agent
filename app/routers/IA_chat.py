from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()

@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return JSONResponse({"message": "Bienvenue sur la page de chat!"})

@router.post("/chat")
def chat_post(request: Request):
    # Ici, tu peux traiter le message utilisateur
    return JSONResponse({"message": "Message reçu!"})
