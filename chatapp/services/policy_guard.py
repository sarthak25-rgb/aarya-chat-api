import os
from groq import Groq
from chatapp.data.policies import POLICIES_TEXT


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

Sorry i Cant help you In this

<BHARAT_CAR_KB>
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
            model="groq-1.5-turbo-16k",
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
