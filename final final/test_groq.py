import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one sentence."}
        ],
        max_tokens=50
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    result = test_groq()
    print(result)
