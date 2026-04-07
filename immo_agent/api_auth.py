from fastapi import FastAPI, Response, Request, Cookie, HTTPException
from pydantic import BaseModel
from . import db_session
# On importe la fonction de chat de ton projet
from agent_memory import interroger_agent 

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuration CORS pour éviter les erreurs réseau dans le navigateur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str

class ChatRequest(BaseModel):
    message: str

# 1. Route de Connexion : Génère le cookie
@app.post("/api/login")
async def login(req: LoginRequest, response: Response):
    user_id = db_session.get_or_create_user(req.email)
    session_id = db_session.create_session(user_id)
    
    # On place le badge (cookie) dans le navigateur
    response.set_cookie(
        key="session_id", 
        value=session_id, 
        httponly=True, # Sécurité : empêche le JS de lire le cookie
        max_age=30*24*60*60 # 30 jours
    )
    return {"status": "success", "message": "Connecté"}

# 2. Route de Chat : Utilise le cookie automatiquement
@app.post("/api/chat")
async def chat(req: ChatRequest, session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Non connecté")
    
    # On vérifie qui est l'utilisateur derrière ce cookie
    user_id = db_session.verify_session(session_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="Session invalide ou expirée")
    
    # On utilise l'id utilisateur comme thread_id pour garder la mémoire
    reponse = interroger_agent(req.message, user_id)
    return {"reply": reponse}

# 3. Servir le Frontend
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# S'assurer que le dossier static existe
os.makedirs("frontend", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_auth:app", host="0.0.0.0", port=8000, reload=True)
