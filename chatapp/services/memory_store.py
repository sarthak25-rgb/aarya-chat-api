# chatapp/services/memory_store.py

conversation_memory = {}

def get_session_history(session_id: str):
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    return conversation_memory[session_id]

def append_message(session_id: str, role: str, content: str):
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []

    conversation_memory[session_id].append({
        "role": role,
        "content": content
    })

# STEP 2: count user messages per session
def count_user_messages(session_id: str) -> int:
    messages = conversation_memory.get(session_id, [])
    return sum(1 for m in messages if m["role"] == "user")
