from openai import OpenAI
from config import OPENAI_API_KEY


def openai_nlp(full_transcript):
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=full_transcript
    )
