import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))

HISTORY_DIR = "history"
os.makedirs(HISTORY_DIR, exist_ok=True)

def get_history_path(context_id):
    return os.path.join(HISTORY_DIR, f"{context_id}.jsonl")

def load_history(context_id):
    history_path = get_history_path(context_id)
    messages = []
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    messages.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue  # Ignore invalid JSON lines
    return messages

def append_to_history(context_id, message):
    history_path = get_history_path(context_id)
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")

def chatgpt_response(prompt, context_id):
    if not prompt:
        return "請提供有效的提示語。"

    messages = load_history(context_id)

    # Add system prompt as the first message
    system_message = {
        "role": "system",
        "content": "你是一隻可愛的貓咪，請在每句話的結尾加上 'meow~'，並且使用可愛的語氣回應。"
    }
    messages = [system_message] + messages

    # Add user's prompt
    user_message = {"role": "user", "content": prompt}
    messages.append(user_message)

    # Call OpenAI API
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        temperature=1.2
    )

    reply = chat_completion.choices[0].message.content

    # Append user message and bot reply to history
    append_to_history(context_id, user_message)
    append_to_history(context_id, {"role": "assistant", "content": reply})

    return reply