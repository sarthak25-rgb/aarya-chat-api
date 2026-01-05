import os
from groq import Groq
from chatapp.data.policies import POLICIES_TEXT

# Groq client — reads ONLY GROQ_API_KEY
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = f"""
You are Aarya, the AI assistant of Bharat Car.

PERSONALITY:
- Friendly
- Polite
- Calm
- Helpful
- Human-like

RULES:
- Answer strictly from policy text
- Do not invent rules
- If policy not found, reply:
  "For more information, please call our support line at 9638794665."

POLICY TEXT:
{POLICIES_TEXT}
"""

def get_policy_answer(user_question: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question}
        ],
        temperature=0.3,
        max_tokens=250
    )
    return response.choices[0].message.content.strip()
