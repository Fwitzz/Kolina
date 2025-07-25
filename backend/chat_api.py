import os
import requests

API_KEY = os.environ.get("MISTRAL_API_KEY", "")
if not API_KEY:
    raise RuntimeError("Set MISTRAL_API_KEY in your environment")

API_URL = "https://api.mistral.ai/v1/chat/completions"

def get_mistral_response(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "mistral-small-latest",  # or choose large/medium
        "messages": [
            {"role": "system", "content": "You are a helpful Linux assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
