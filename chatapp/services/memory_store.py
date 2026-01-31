import os
from groq import Groq
from chatapp.data.policies import POLICIES_TEXT


REFUSAL_TEXT = "Sorry i Cant help you In this"


SYSTEM_PROMPT = f"""
You are Aarya, the official AI assistant of Bharat Car.

You are a restricted company assistant.

Your ONLY allowed source of information is the text inside <BHARAT_CAR_KB>.

You must follow these rules strictly.

ALLOWED:
- Answer only if the information is explicitly present in <BHARAT_CAR_KB>.
- Keep answers short, factual and professional.
- Reply in the same language as the user.

NOT ALLOWED:
- Using general knowledge.
- Making assumptions.
- Adding examples.
- Explaining beyond the policy text.
- Asking clarifying questions.
- Offering help outside the Bharat Car domain.
- Being conversational.
- Mentioning policies, documents or the knowledge base.
- Mentioning that you are restricted.

OUT OF SCOPE HANDLING:

If the user's question is NOT related to Bharat Car
OR
if the answer is NOT explicitly present in <BHARAT_CAR_KB>,

reply with EXACTLY the following text and nothing else:

{REFUSAL_TEXT}

<BHARAT_CAR_KB>
{POLICIES_TEXT}
"""


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is missing")

    return Groq(api_key=api_key)


def _post_guard(answer: str) -> str:
    """
    Hard safety guard to block conversational or out-of-scope replies.
    """
    if not answer:
        return REFUSAL_TEXT

    cleaned = answer.strip()

    # exact refusal is always allowed
    if cleaned == REFUSAL_TEXT:
        return cleaned

    banned_phrases = [
        "happy to help",
        "i can help",
        "i can try",
        "i would be happy",
        "i'm aarya",
        "i am aarya",
        "what kind of",
        "how can i help",
        "clarify",
        "general guidance",
        "point you in the right",
        "feel free",
        "let me know",
    ]

    low = cleaned.lower()

    if any(p in low for p in banned_phrases):
        return REFUSAL_TEXT

    return cleaned


def get_policy_answer(user_question: str) -> str:
    """
    Generate a strictly policy-bound answer for Aarya (Bharat Car).
    No conversation memory is used.
    """
    try:
        client = get_groq_client()

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question}
            ],
            temperature=0,
            top_p=1,
            max_tokens=200
        )

        raw_answer = response.choices[0].message.content

        return _post_guard(raw_answer)

    except Exception as e:
        print("POLICY GUARD ERROR >>>", e)
        return REFUSAL_TEXT
