from app.core.templating import templates
from app.services import user_db_simple
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
import psycopg2

router = APIRouter()

@router.get("/connexion")
async def connexion(request: Request):
    return templates.TemplateResponse("connexion.html", {"request": request})

@router.post("/connexion")
async def connexion_post(request: Request):
    form_data = await request.form()
    username = form_data.get("email")
    password = form_data.get("password")
    
    user_id = user_db_simple.verify_user(username, password)
    if user_id is not None:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="user_id",
            value=str(user_id),
            httponly=True,
            samesite="lax",
        )
        return response

    return templates.TemplateResponse("connexion.html", {"request": request, "error": "Identifiants invalides"})
    
@router.get("/inscription")
async def inscription(request: Request):
    return templates.TemplateResponse("inscription.html", {"request": request})


@router.post("/inscription")
async def inscription_post(request: Request):
    form_data = await request.form()
    email = form_data.get("email")
    password = form_data.get("password")
    confirm_password = form_data.get("confirm_password")

    if not email or not password:
        return templates.TemplateResponse(
            "inscription.html",
            {"request": request, "error": "Email et mot de passe obligatoires."},
            status_code=400,
        )

    if password != confirm_password:
        return templates.TemplateResponse(
            "inscription.html",
            {"request": request, "error": "Les mots de passe ne correspondent pas."},
            status_code=400,
        )

    try:
        user_db_simple.init_user_conversation_schema()
        user_id = user_db_simple.add_user(email, password)
        print(f"Utilisateur créé avec l'ID : {user_id}")
    except psycopg2.IntegrityError:
        user_db_simple.conn.rollback()
        return templates.TemplateResponse(
            "inscription.html",
            {"request": request, "error": "Cet email existe deja."},
            status_code=409,
        )

    return RedirectResponse(url="/connexion", status_code=303)



@router.get("/user/{user_id}/conversations")
async def get_user_conversations(user_id: int, request: Request):
    conversations = user_db_simple.get_user_conversations(user_id)
    return JSONResponse({"conversations": conversations})

