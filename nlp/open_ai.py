import openai
from utils.config import OPENAI_API_KEY


def nlp_openai(question):
    try:
        openai.api_key = OPENAI_API_KEY
        openai_client = openai
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                  "role": "user",
                  "content": question
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as error:
        print(error)
