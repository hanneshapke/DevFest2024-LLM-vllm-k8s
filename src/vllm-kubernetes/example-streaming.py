# test openai streaming
import sys
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="token-abc123",
)

system_prompt = "You are a helpful AI assistant excellent in writing poetry."
user_prompt = "Please write a Haiku about the amazing DevFest Silicon Valley and Responsible AI"


if __name__ == "__main__":
    response = client.chat.completions.create(
        model="google/gemma-2-2b-it",
        messages=[
            {"role": "system", "content": system_prompt },
            {"role": "user", "content": user_prompt}
        ],
        stream=True)

    s = ""
    for chunk in response:
        s += chunk.choices[0].delta.content
        sys.stdout.write(chunk.choices[0].delta.content)
