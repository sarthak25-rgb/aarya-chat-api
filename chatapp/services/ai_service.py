import os
from dotenv import load_dotenv
from openai import OpenAI
from chatapp.services.memory_store import append_message, count_user_messages

load_dotenv()

# ================= CONFIG =================
MAX_MESSAGES_PER_SESSION = 15

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------- SYSTEM PROMPT (MUST BE ON TOP) --------
SYSTEM_PROMPT = """
You are Aarya, a polite and professional AI assistant from Bharat Car.

Rules:
- Reply in 1–2 short lines only.
- English input → English reply.
- Hindi input → Hinglish reply (Roman letters only).
- Calm, professional, helpful tone.
- Ask only one question at a time.
- Do NOT remember previous questions.
- Always stay relevant to the current message only.
- Do NOT offer step-by-step help.
- Do NOT ask follow-up questions unless absolutely necessary.
"""

INTRO_MESSAGE = "Hello 😊 I’m Aarya from Bharat Car. How can I assist you today?"

SIMPLE_BOOKING_GUIDANCE = (
    "Aap Bharat Car app mein jaakar apni pasand ki car select kijiye, "
    "phir pickup aur drop location set karke booking confirm kar sakte hain."
)

BOOKING_KEYWORDS = [
    "how can i book",
    "how to book",
    "book a car",
    "booking process",
    "kaise car book",
    "kese car book",
    "car book karu",
    "car booking"
]

# ================= MAIN FUNCTION =================
def generate_reply(session_id: str, user_message: str) -> str:
    try:
        # 1️⃣ Greet ONLY on first (empty) message
        if not user_message or user_message.strip() == "":
            reply = INTRO_MESSAGE
            append_message(session_id, "assistant", reply)
            return reply

        # 2️⃣ STEP 3: Enforce 15-message session limit
        if count_user_messages(session_id) >= MAX_MESSAGES_PER_SESSION:
            return (
                "You’ve reached the maximum number of messages for this chat 😊 "
                "Please start a new chat to continue."
            )

        msg_lower = user_message.lower()

        # 3️⃣ Simple booking guidance (no steps, no follow-up)
        if any(k in msg_lower for k in BOOKING_KEYWORDS):
            reply = SIMPLE_BOOKING_GUIDANCE
            append_message(session_id, "user", user_message)
            append_message(session_id, "assistant", reply)
            return reply

        # 4️⃣ Normal AI response
        response = client.responses.create(
            model="gpt-5-nano-2025-08-07",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.output_text or "Sure. Please tell me how I can assist."

    except Exception as e:
        print("OPENAI ERROR >>>", e)
        reply = "Sorry, I’m unable to respond right now."

    # 5️⃣ Store conversation (no context reuse logic)
    append_message(session_id, "user", user_message)
    append_message(session_id, "assistant", reply)

    return reply
