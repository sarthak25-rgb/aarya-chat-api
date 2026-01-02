from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
load_dotenv()


from chatapp.routes.chat import router as chat_router
from chatapp.routes.predefined import router as predefined_router

app = FastAPI(
    title="Bharat Car Chatbot",
    version="1.0.0"
)

# API routes
app.include_router(chat_router, prefix="/api/chat")
app.include_router(predefined_router, prefix="/api/predefined")

# ---------- FRONTEND ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

@app.get("/")
def serve_ui():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))
