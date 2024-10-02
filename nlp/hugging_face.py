from utils.config import HUGGING_FACE_API_KEY
from requests import post


def nlp_hugging_face(question):
    try:
        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        api_url = "https://api-inference.huggingface.co/models/gpt2"
        payload = {"inputs": question}
        response = post(api_url, headers=headers, json=payload).json()
        return response[0]["generated_text"]
    except Exception as error:
        print(error)
