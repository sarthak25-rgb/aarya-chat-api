from chatapp.services.ai_service import generate_reply

def chat_handler(data: dict):
    session_id = data.get("session_id")
    user_message = data.get("message")

    if not session_id:
        return {
            "success": False,
            "error": "session_id is required"
        }

    if not user_message:
        return {
            "success": False,
            "error": "message is required"
        }

    reply = generate_reply(session_id, user_message)

    return {
        "success": True,
        "reply": reply,
        "session_id": session_id
    }
