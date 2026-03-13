import asyncio
import selectors
import sys
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# Fix for Windows: psycopg async requires SelectorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.DefaultEventLoopPolicy()
    )
    loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.set_event_loop(loop)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from app.routers import IA_chat ,connexion
from app.core.templating import templates
from app.services.agent import AgentSingleton
from app.services import user_db_simple
from dotenv import load_dotenv
from pathlib import Path
from contextlib import asynccontextmanager
load_dotenv()


DB_URI = "postgresql://admin:mdp@localhost:5432/ma_base_de_donnees"

@asynccontextmanager
async def lifespan(app: FastAPI):
    user_db_simple.init_user_conversation_schema()
    async with AsyncPostgresSaver.from_conn_string(DB_URI) as saver:
        await saver.setup()
        AgentSingleton.initialize(saver)
        yield
        AgentSingleton.reset()


app = FastAPI(lifespan=lifespan)

app.include_router(IA_chat.router)
app.include_router(connexion.router)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return RedirectResponse(url=f"/conversation")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)