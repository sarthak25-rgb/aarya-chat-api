from fastapi import APIRouter
from pydantic import BaseModel
from chatapp.services.policy_guard import get_policy_answer

router = APIRouter()  # ❌ removed prefix here

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/")
def chat(req: ChatRequest):
    user_message = req.message.strip()
    reply = get_policy_answer(user_message)
    return {"reply": reply}
