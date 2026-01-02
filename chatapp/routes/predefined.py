from fastapi import APIRouter
from pydantic import BaseModel
from chatapp.services.predefined_faq import PREDEFINED_FAQ

router = APIRouter()


class PredefinedQuestionRequest(BaseModel):
    question: str


@router.post("/predefined-question")
def handle_predefined_question(payload: PredefinedQuestionRequest):
    question = payload.question.strip()

    answer = PREDEFINED_FAQ.get(
        question,
        "Sorry, I don't have an answer for this question."
    )

    return {
        "type": "predefined",
        "question": question,
        "answer": answer
    }
