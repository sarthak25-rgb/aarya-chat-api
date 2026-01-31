from fastapi import APIRouter
from pydantic import BaseModel

from chatapp.services.predefined_faq import PREDEFINED_FAQ
from chatapp.services.policy_guard import get_policy_answer

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str


@router.post("/")
def predefined_chat(req: ChatRequest):
    user_message = req.message.strip()

    # 1. exact FAQ match
    if user_message in PREDEFINED_FAQ:
        return {"reply": PREDEFINED_FAQ[user_message]}

    # 2. fallback to strict policy bot
    reply = get_policy_answer(user_message)

    return {"reply": reply}
