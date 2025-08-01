import requests
import time
import os

API_KEY = os.getenv("KANDINSKY_API_KEY")
HEADERS = {
    "X-Key": f"Key {API_KEY}"
}
BASE_URL = "https://api.fusionbrain.ai"

def generate_image(prompt: str, model_id: int = 2) -> str:
    init_resp = requests.post(
        f"{BASE_URL}/image/generate",
        headers=HEADERS,
        json={"prompt": prompt, "model_id": model_id}
    )
    uuid = init_resp.json().get("uuid")
    for _ in range(30):
        time.sleep(2)
        status = requests.get(f"{BASE_URL}/image/status/{uuid}", headers=HEADERS).json()
        if status.get("status") == "done":
            return status["images"][0]
    return None
