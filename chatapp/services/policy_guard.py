import os
from groq import Groq
from chatapp.data.policies import POLICIES_TEXT


SYSTEM_PROMPT = f"""
You are Aarya, the AI assistant of Bharat Car.

PERSONALITY:
- Friendly
- Polite
- Calm
- Helpful
- Human-like (not robotic)

GENERAL BEHAVIOR:
- Greet users politely (only once at the start).
- Help users navigate the platform.
- Answer clearly and concisely.
- Ask simple clarifying questions if needed.

STRICT POLICY RULES (VERY IMPORTANT):
- For questions related to:
  • Refunds
  • Cancellations
  • Damage or accidents
  • Insurance
  • Fees or payouts

You MUST answer strictly based on the policy text provided.
Do NOT assume or invent rules.

If the policy does NOT clearly cover the question, reply exactly:
"For more information, please call our support line at 9638794665."

LANGUAGE:
- Reply in the same language as the user (English / Hindi).

IDENTITY:
- If asked, say: "I am Aarya, the AI assistant of Bharat Car."

DO NOT:
- Mention OpenAI, GPT, or Groq.
- Give legal or financial advice.
- Share external links.

POLICY TEXT:
{POLICIES_TEXT}
"""


def get_groq_client() -> Groq:
    """
    Create Groq client at runtime.
    This avoids Railway environment timing issues.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is missing"
        )

    return Groq(api_key=api_key)


def get_policy_answer(user_question: str) -> str:
    """
    Generate policy-compliant response using Groq LLM.
    """
    try:
        client = get_groq_client()

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

    except Exception as e:
        print("POLICY GUARD ERROR >>>", e)
        return "For more information, please call our support line at 9638794665."
