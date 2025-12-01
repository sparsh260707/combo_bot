# helpers/chat_helper.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def ai_reply(prompt: str, model: str = "gpt-3.5-turbo"):
    """Get AI response using OpenAI chat model."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"AI Reply Error: {e}")
        return "Sorry, I couldn't generate a reply."
