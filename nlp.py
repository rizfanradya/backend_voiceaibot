from config import HUGGING_FACE_API_KEY
from requests import post


def natural_language_processing(question):
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    api_url = "https://api-inference.huggingface.co/models/gpt2"
    payload = {"inputs": question}
    response = post(api_url, headers=headers, json=payload).json()
    return response[0]["generated_text"]
